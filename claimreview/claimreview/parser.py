import json
import microdata
import dateutil.parser

class ClaimReviewParser:
    def parse(self, response):
        items = self.get_microdata_items(response)

        scripts = response.css('script[type="application/ld+json"]::text').extract()

        for script in scripts:
            item = json.loads(script)

            if '@type' in item and (item['@type'] == 'ClaimReview' or 'ClaimReview' in item['@type']):
                rr = item.get('reviewRating')
                ir = item.get('itemReviewed')

                items.append(
                    dict(
                        type=item.get('@type'),
                        datePublished=self.parse_date(item.get('datePublished')),
                        dateModified=self.parse_date(item.get('dateModified')),
                        url=item.get('url'),
                        author=[
                            dict(
                                type=a.get('@type'),
                                name=a.get('name'),
                                url=a.get('url'),
                                twitter=a.get('twitter'),
                                sameAs=[str(s) for s in self.listify(a.get('sameAs'))]
                            ) for a in self.listify(item.get('author'))
                        ],
                        claimReviewed=item.get('claimReviewed'),
                        reviewRating=dict(
                            type=rr.get('@type'),
                            ratingValue=rr.get('ratingValue'),
                            bestRating=rr.get('bestRating'),
                            worstRating=rr.get('worstRating'),
                            alternateName=rr.get('alternateName')
                        ),
                        itemReviewed=dict(
                            type=ir.get('@type'),
                            author=[
                                dict(
                                    type=a.get('@type'),
                                    name=a.get('name'),
                                    url=a.get('url'),
                                    twitter=a.get('twitter'),
                                    sameAs=[str(s) for s in self.listify(a.get('sameAs'))]
                                ) for a in self.listify(ir.get('author'))
                            ],
                            datePublished=self.parse_date(ir.get('datePublished')),
                            sameAs=[str(s) for s in self.listify(ir.get('sameAs'))]
                        ),
                ))

        return items

    def get_microdata_items(self, response):
        items = microdata.get_items(response.text)

        result = []

        for item in items:
            if 'ClaimReview' in str(item.itemtype[-1]):
                rr = item.get('reviewRating')
                img = item.get('image')
                ir = item.get('itemReviewed');

                result.append(
                    dict(
                        type=str(item.itemtype[-1]),
                        datePublished=self.parse_date(item.get('datePublished')),
                        dateModified=self.parse_date(item.get('dateModified')),
                        url=str(item.get('url')),
                        author=self.microdata_authors_from(item),
                        image=dict(
                            type=str(img.itemtype[-1]),
                            url=str(img.get('url')),
                            width=img.get('width'),
                            height=img.get('height')
                        ) if img else None,
                        claimReviewed=item.get('claimReviewed'),
                        reviewRating=dict(
                            type=str(rr.itemtype[-1]),
                            ratingValue=rr.get('ratingValue'),
                            bestRating=rr.get('bestRating'),
                            worstRating=rr.get('worstRating'),
                            alternateName=rr.get('alternateName') or rr.get('name')
                        ),
                        itemReviewed=dict(
                            type=str(ir.itemtype[-1]),
                            author=self.microdata_authors_from(ir),
                            datePublished=self.parse_date(ir.get('datePublished')),
                            sameAs=[str(s) for s in ir.get_all('sameAs')]
                        ),
                        keywords=str(item.get('keywords')) if item.get('keywords') else None,
                    )
                )

        return result;


    def microdata_authors_from(self, item):
        return [
            dict(
                type=str(a.itemtype[-1]),
                name=a.get('name'),
                url=str(a.get('url')) if a.get('url') else None,
                twitter=str(a.get('twitter')) if a.get('twitter') else None,
                sameAs=[str(s) for s in a.get_all('sameAs')]
            ) for a in item.get_all('author')
        ]

    def listify(self, obj):
        if obj == None:
            return []
        elif isinstance(obj, list):
            return obj
        else:
            return [obj]

    def parse_date(self, dateString):
        if dateString is not None:
            return dateutil.parser.parse(dateString)
        else:
            return None


