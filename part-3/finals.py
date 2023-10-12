import pandas as pd
reddit = pd.read_csv("reddit_db.csv")
reddit.drop(labels=['Unnamed: 0.1','Unnamed: 0'],axis=1,inplace=True)
reddit['new_created'] = pd.to_datetime(reddit['new_created'])
reddit['collected_on'] = reddit['new_created'].dt.date
hacker_news = pd.read_csv("hn_data.csv", header = None,names=['id','by','descendants','score','time','title','url'])
from datetime import datetime
hacker_news['new_created']=hacker_news['time'].map(lambda x: str(datetime.fromtimestamp(x)))
hacker_news['new_created'] = pd.to_datetime(hacker_news['new_created'])
hacker_news['collected_on'] = hacker_news['new_created'].dt.date
hacker_news['platform']='Hacker News'
reddit['platform']='Reddit'
DB_df=pd.concat([reddit,hacker_news])
DB_df['collected_date']=pd.to_datetime(DB_df['new_created'], format='%Y-%m-%d')

# sentiment analysis
import matplotlib.pyplot as pl
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentiment_lib = SentimentIntensityAnalyzer()
def get_score(x):
    try:
        val = sentiment_lib.polarity_scores(x)['compound']
    except:
        val = None
    return val

def get_class(x):
    if x==0:
        return 'Neutral'
    elif x<0:
        return 'Negative'
    else:
        return 'Positive'

DB_df['sentiment_analysis_score'] = DB_df['title'].apply(lambda x:get_score(str(x)))
DB_df["class"] = DB_df['sentiment_analysis_score'].apply(lambda x: get_class(x))
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"

#anlaysis with nltk and wordcloud and tf-idf top words
import dash
from dash.dependencies import Input, Output
from dash import html,dcc
import dash_bootstrap_components as dbc
postive_score=len(DB_df[DB_df['class']=='Positive'])*100/len(DB_df)
negative_score=len(DB_df[DB_df['class']=='Negative'])*100/len(DB_df)
neutral_score=len(DB_df[DB_df['class']=='Neutral'])*100/len(DB_df)


import re
import nltk

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
import re
stop_words = set(stopwords.words("english"))


from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def get_corpus(df):
    corpus = []
    df['word_count'] = df['title'].apply(lambda x: len(str(x).split(" ")))
    ds_count = len(df.word_count)
    for i in range(0, ds_count):
        try:
            # Remove punctuation
            text = re.sub('[^a-zA-Z]', ' ', str(df['title'][i]))

            # Convert to lowercase
            text = text.lower()

            # Remove tags
            text=re.sub("</?.*?>"," <> ",text)

            # Remove special characters and digits
            text=re.sub("(\\d|\\W)+"," ",text)

            # Convert to list from string
            text = text.split()

            # Stemming
            ps=PorterStemmer()

            # Lemmatisation
            lem = WordNetLemmatizer()
            text = [lem.lemmatize(word) for word in text if not word in  
                    stop_words] 
            text = " ".join(text)
        except:
            text=''
        corpus.append(text)
    return corpus

import datetime
value1='2022-10-29'
value2='2022-12-5'
start_date = datetime.date(int(value1.split('-')[0]),int(value1.split('-')[1]),int(value1.split('-')[2]))
end_date = datetime.date(int(value2.split('-')[0]),int(value2.split('-')[1]),int(value2.split('-')[2]))

# the below functions are to generate the plots
def get_plat_total(plat='Reddit',cltype='Neutral',st_date=start_date,ed_date=end_date,df_t=DB_df):
    if plat == 'All':
        c=len(df_t)
        return len(df_t.loc[ df_t['class']== cltype])*100/c
    else:
        df_t = df_t.loc[df_t['platform']==plat]
        c=len(df_t)
        return len(df_t.loc[ df_t['class']== cltype])*100/c


def fig_world_trend(plat='Reddit',st_date=start_date,ed_date=end_date,df_t=DB_df):

    df1=df_t[df_t['platform']==plat]
    df_grouped = (
        df1.groupby(
            df1['collected_on']
        )['platform'].count().rename('Count').to_frame()
    )

    fig = px.line(
        df_grouped, y='Count', title='Daily collected posts trend for {}'.format(plat),height=600,color_discrete_sequence =['maroon'],hover_data=['Count']
    )
    fig.update_layout(title_x=0.5,plot_bgcolor='#F2DFCE',paper_bgcolor='#F2DFCE',xaxis_title="Date",yaxis_title='count')
    return fig

def get_wordcloud_fig(plat='Reddit',st_date=start_date,ed_date=end_date,df_t=DB_df):
    corp_df = df_t.loc[df_t['platform']==plat]
    corpus=get_corpus(corp_df)
    wordcloud = WordCloud(
                              background_color='white',
                              stopwords=stop_words,
                              max_words=100,
                              max_font_size=50, 
                              random_state=42
                             ).generate(str(corpus))
    
    fig= px.imshow(wordcloud,title='word cloud for {}'.format(plat))
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(visible=False, showticklabels=False)
    fig.update_layout(title_x=0.5,plot_bgcolor='#F2DFCE',paper_bgcolor='#F2DFCE')
    return fig

def get_top_n_words(corpus, n=None):
    vec = CountVectorizer().fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in      
                   vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                       reverse=True)
    return words_freq[:n]

def plot_top_words(plat='Reddit',st_date=start_date,ed_date=end_date,df_t=DB_df):
    corp_df = df_t[df_t['platform']==plat]
    corpus=get_corpus(corp_df)
    top_words = get_top_n_words(corpus, n=20)
    top_df = pd.DataFrame(top_words)
    top_df.columns=["Keyword", "Frequency"]

    fig = px.bar(top_df,x='Keyword', y='Frequency', title='Top terms in trend for {}'.format(plat))
    fig.update_layout(title_x=0.5,xaxis_title='Words',yaxis_title='count',plot_bgcolor='#F2DFCE',paper_bgcolor='#F2DFCE')
    fig.update_xaxes(tickangle=45)
    return fig

# from here the dash module code for the front end part
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Anlaysis of trends'

# styling
colors = {
    'background': '#111111',
    'bodyColor':'#F2DFCE',
    'text': '#7FDBFF'
}
def get_page_heading_style():
    return {'backgroundColor': colors['background']}


def get_page_heading_title():
    return html.H1(children='Anlaysis of trends',
                                        style={
                                        'textAlign': 'center',
                                        'color': colors['text']
                                    })

def get_page_heading_subtitle():
    return html.Div(children='Visualize Anlaysis of trends data generated from sources Twitter, Reddit and Hacker News.',
                                         style={
                                             'textAlign':'center',
                                             'color':colors['text']
                                         })

def generate_page_header():
    main_header =  dbc.Row(
                            [
                                dbc.Col(get_page_heading_title(),md=12)
                            ],
                            align="center",
                            style=get_page_heading_style()
                        )
    subtitle_header = dbc.Row(
                            [
                                dbc.Col(get_page_heading_subtitle(),md=12)
                            ],
                            align="center",
                            style=get_page_heading_style()
                        )
    header = (main_header,subtitle_header)
    return header

def get_plat_list():
    f=DB_df['platform'].unique()
#     f.append('All')
    return f

def create_dropdown_list(plat_list):
    dropdown_list = []
    for plat in sorted(plat_list):
        tmp_dict = {'label':plat,'value':plat}
        dropdown_list.append(tmp_dict)
    return dropdown_list

def get_plat_dropdown(id):
    return html.Div([
                        html.Label('Select Platform'),
                        dcc.Dropdown(id='my-id'+str(id),
                            options=create_dropdown_list(get_plat_list()),
                            value='Reddit'
                        ),
                        html.Div(id='my-div'+str(id))
                    ])

from datetime import datetime as dt

def get_dates():
    return html.Div([
        dcc.DatePickerRange(
            id='my-date-picker-range', 
            calendar_orientation='horizontal', 
            day_size=39,
            end_date_placeholder_text="Return", 
            with_portal=False,  
            first_day_of_week=0,  
            reopen_calendar_on_clear=True,
            is_RTL=False, 
            clearable=True,  
            number_of_months_shown=1, 
            min_date_allowed=dt(2022, 10, 29), 
            max_date_allowed=dt(2022, 12, 5),  
            initial_visible_month=dt(2022, 10, 1),  
            start_date=dt(2022, 10, 29).date(),
            end_date=dt(2022, 12, 5).date(),
            display_format='MMM Do, YY', 
            month_format='MMMM, YYYY',  

            persistence=True,
            persisted_props=['start_date'],
            persistence_type='session',  

            updatemode='singledate'  
        )
    ])
# below 3 functions for the graphs in dash call
def graph1():
    return dcc.Graph(id='graph1',figure=fig_world_trend(plat='Reddit'))

def graph2():
    return dcc.Graph(id='graph2',figure=get_wordcloud_fig(plat='Reddit'))

def graph3():
    return dcc.Graph(id='graph3',figure=plot_top_words(plat='Reddit'))

# for the card of sentiment scores
def generate_card_content(card_header,card_value,overall_value):
    card_head_style = {'textAlign':'center','fontSize':'150%'}
    card_body_style = {'textAlign':'center','fontSize':'200%'}
    card_header = dbc.CardHeader(card_header,style=card_head_style)
    card_body = dbc.CardBody(
        [
            html.H5(f"{int(card_value):,}", className="card-title",style=card_body_style),
            html.P(
                "Across all Platform: {:,}".format(overall_value),
                className="card-text",style={'textAlign':'center'}
            ),
        ]
    )
    card = [card_header,card_body]
    return card

def generate_cards(plat='Reddit',st_date=start_date,ed_date=end_date,df_t=DB_df):
    net_plat_total = get_plat_total(plat,'Neutral',st_date,ed_date,df_t)
    neg_plat_total = get_plat_total(plat,'Negative',st_date,ed_date,df_t)
    pos_plat_total = get_plat_total(plat,'Positive',st_date,ed_date,df_t)
    cards = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Card(generate_card_content("Positive",pos_plat_total,postive_score), color="success", inverse=True),md=dict(size=2,offset=3)),
                    dbc.Col(dbc.Card(generate_card_content("Neutral",net_plat_total,neutral_score), color="warning", inverse=True),md=dict(size=2)),
                    dbc.Col(dbc.Card(generate_card_content("Negative",neg_plat_total,negative_score),color="dark", inverse=True),md=dict(size=2)),
                ],
                className="mb-4",
            ),
        ],id='card1'
    )
    return cards


# this one is for the whole page layout
def generate_layout():
    page_header = generate_page_header()
    layout = dbc.Container(
        [
            page_header[0],
            page_header[1],
            html.Hr(),
            generate_cards(),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(get_dates(),md=dict(size=4,offset=4))                    
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(get_plat_dropdown(id=1),md=dict(size=4,offset=4))                    
                ]
            ),
            dbc.Row(
                [                
                    dbc.Col(graph1(),md=dict(size=6,offset=3))
                ],
                align="center",

            ),
            dbc.Row(
                [                
                    dbc.Col(graph2(),md=dict(size=6,offset=3))
                ],
                align="center",

            ),
            dbc.Row(
                [                
                    dbc.Col(graph3(),md=dict(size=6,offset=3))
                ],
                align="center",

            ),
        ],fluid=True,style={'backgroundColor': colors['bodyColor']}
    )
    return layout
# calling layout
app.layout = generate_layout()


@app.callback(
    [Output(component_id='graph1',component_property='figure'), 
     Output(component_id='graph2',component_property='figure'),
     Output(component_id='graph3',component_property='figure'),
    Output(component_id='card1',component_property='children')],
    [Input(component_id='my-id1',component_property='value'),
    Input(component_id='my-date-picker-range', component_property='start_date'),
    Input(component_id='my-date-picker-range', component_property='end_date')] 
)
def update_output_div(input_value1,input_value2,input_value3):
    s_d=DB_df.loc[(DB_df['collected_date'] >= input_value2) & (DB_df['collected_date'] < input_value3) & (DB_df['platform'] == input_value1)]
    print('btw',len(s_d))
    return fig_world_trend(input_value1,input_value2,input_value3,s_d),get_wordcloud_fig(input_value1,input_value2,input_value3,s_d),plot_top_words(input_value1,input_value2,input_value3,s_d),generate_cards(input_value1,input_value2,input_value3,s_d)

app.run_server(host= '0.0.0.0',debug=False)
