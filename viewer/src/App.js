import React, { Component } from 'react';
import './App.css';

import 'searchkit/release/theme.css';
import moment from 'moment';
import langs from 'langs';

import {
    SearchkitManager,
    SearchkitProvider,
    SearchBox,
    RefinementListFilter,
    Pagination,
    HierarchicalMenuFilter,
    HitsStats,
    SortingSelector,
    NoHits,
    ResetFilters,
    RangeFilter,
    NumericRefinementListFilter,
    ViewSwitcherHits,
    ViewSwitcherToggle,
    DynamicRangeFilter,
    InputFilter,
    GroupedSelectedFilters,
    Layout,
    TopBar,
    LayoutBody,
    LayoutResults,
    ActionBar,
    ActionBarRow,
    SideBar,
    SelectedFilters,
    Hits
} from 'searchkit';

const searchkit = new SearchkitManager('https://int.faktisk.no/claimreviews/');

const FactCheckItem = ({ bemBlocks, result: { _source } }) => (
    <div className="factcheck-item">
        {_source.image ? <img src={_source.image.url} /> : null}

        <p>
            <small className="muted">
                Rated <strong>{_source.reviewRating.alternateName}</strong> by{' '}
                {_source.author.map(e => e.name)}
            </small>

            <small className="muted">
                {' '}
                @{' '}
                <a href={_source.url} target="_blank">
                    {_source.datePublished
                        ? moment(_source.datePublished).format('LLL')
                        : 'Unknown date'}
                </a>
            </small>
        </p>

        <blockquote>
            <p>{_source.claimReviewed}</p>

            <footer>
                –{' '}
                {_source.itemReviewed && _source.itemReviewed.author
                    ? _source.itemReviewed.author.map(a => (
                          <cite key={a.name}>
                              {a.name} ({a.type.split('/').slice(-1)})
                          </cite>
                      ))
                    : null}{' '}
                @{' '}
                {_source.itemReviewed.datePublished
                    ? moment(_source.itemReviewed.datePublished).format('LLL')
                    : 'Unknown date'}
            </footer>
        </blockquote>

        <pre>{/*JSON.stringify(_source, null, 2)*/}</pre>
    </div>
);

const codeToLang = str => {
    const lang = langs.where('1', str) || langs.where('2', str) || langs.where('3', str);

    if (lang) {
        return lang.name;
    } else {
        return str;
    }
}


const LanguageRefinementOption = props => (
    <div
        className={props.bemBlocks
            .option()
            .state({ selected: props.selected })
            .mix(props.bemBlocks.container('item'))}
        onClick={props.onClick}
    >
        <div className={props.bemBlocks.option('text')}>{codeToLang(props.label)}</div>
        <div className={props.bemBlocks.option('count')}>{props.count}</div>
    </div>
);

const App = () => (
    <SearchkitProvider searchkit={searchkit}>
        <Layout>
            <TopBar>
                <SearchBox
                    autofocus={true}
                    searchOnChange={true}
                    prefixQueryFields={[
                        'claimReviewed^1',
                        'author.name^1',
                        'itemReviewed.author.name^1'
                    ]}
                />
            </TopBar>
            <LayoutBody>
                <SideBar>
                    <RefinementListFilter
                        id="language"
                        title="Language"
                        field="language.keyword"
                        operator="OR"
                        itemComponent={LanguageRefinementOption}
                        size={10}
                    />
                    <RefinementListFilter
                        id="authors"
                        title="Authors"
                        field="author.name.keyword"
                        operator="OR"
                        size={10}
                    />
                    <RefinementListFilter
                        id="claimants"
                        title="Claimants"
                        field="itemReviewed.author.name.keyword"
                        operator="OR"
                        size={10}
                    />
                    <RefinementListFilter
                        id="ratings"
                        title="Ratings"
                        field="reviewRating.alternateName.keyword"
                        operator="OR"
                        size={10}
                    />
                </SideBar>
                <LayoutResults>
                    <ActionBar>
                        <ActionBarRow>
                            <HitsStats />
                            <SortingSelector
                                options={[
                                    {
                                        label: 'Published',
                                        field: 'datePublished',
                                        order: 'desc',
                                        defaultOption: true
                                    },
                                    {
                                        label: 'Relevance',
                                        field: '_score',
                                        order: 'desc',
                                    },
                                    {
                                        label: 'Claim published',
                                        field: 'itemReviewed.datePublished',
                                        order: 'desc'
                                    }
                                ]}
                            />
                        </ActionBarRow>

                        <ActionBarRow>
                            <SelectedFilters />
                            <ResetFilters />
                        </ActionBarRow>
                    </ActionBar>

                    <Hits
                        mod="sk-hits-list"
                        hitsPerPage={20}
                        itemComponent={FactCheckItem}
                        sourceFilter={null}
                    />
                    <NoHits suggestionsField="claimReviewed" />

                    <Pagination showNumbers />
                </LayoutResults>
            </LayoutBody>
        </Layout>
    </SearchkitProvider>
);

export default App;
