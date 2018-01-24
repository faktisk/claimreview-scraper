import React, { Component } from 'react';
import './App.css';

import 'searchkit/release/theme.css';
import moment from 'moment';

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

const FactCheckItem = ({bemBlocks, result: {_source}}) => (
    <div className="factcheck-item">
        <blockquote>
            <p>
                <a href={_source.url} target="_blank">
                    {_source.claimReviewed}
                </a>
            </p>

            <footer>
                {
                    _source.itemReviewed && _source.itemReviewed.author ? (
                        _source.itemReviewed.author.map(a => (
                            <cite key={a.name}>
                                {a.name} ({a.type.split('/').slice(-1)})
                            </cite>
                        ))
                    ) : null
                }
            </footer>
        </blockquote>

        <p>
            <small className="muted">Rated <strong>{_source.reviewRating.alternateName}</strong> by {_source.author.map(e => e.name)}</small>
            {_source.datePublished ? <small className="muted"> @ {moment(_source.datePublished).format('LLL')}</small> : null}
        </p>


        <pre>{/*JSON.stringify(_source, null, 2)*/}</pre>

   </div>

)

const App = () => (
    <SearchkitProvider searchkit={searchkit}>
        <Layout>
            <TopBar>
                <SearchBox
                    autofocus={true}
                    searchOnChange={true}
                    prefixQueryFields={[
                        'claimReviewed^1',
                    ]}
                />
            </TopBar>
            <LayoutBody>
                <SideBar>
                    <RefinementListFilter
                        id="authors"
                        title="Authors"
                        field="author.name.keyword"
                        operator="AND"
                        size={10}
                    />
                    <RefinementListFilter
                        id="ratings"
                        title="Ratings"
                        field="reviewRating.alternateName.keyword"
                        operator="AND"
                        size={50}
                    />
                </SideBar>
                <LayoutResults>
                    <ActionBar>
                        <ActionBarRow>
                            <HitsStats />
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
                </LayoutResults>
            </LayoutBody>
        </Layout>
    </SearchkitProvider>
);

export default App;
