import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os
import numpy as np

def load_tweets(file_path='tweets_with_topics.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        df = pd.DataFrame(data['tweets'])
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        metrics_df = pd.json_normalize(df['public_metrics'])
        df = pd.concat([df.drop('public_metrics', axis=1), metrics_df], axis=1)
        
        return df

def save_plotly_figure(fig, filename):
    def convert_numpy(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            if np.isnan(obj):
                return None
            return float(obj)
        elif isinstance(obj, (list, tuple)):
            return [convert_numpy(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: convert_numpy(value) for key, value in obj.items()}
        return obj
    
    fig_dict = fig.to_dict()
    
    for trace in fig_dict['data']:
        if 'x' in trace:
            trace['x'] = convert_numpy(trace['x'])
        if 'y' in trace:
            trace['y'] = convert_numpy(trace['y'])
        if 'z' in trace:
            trace['z'] = convert_numpy(trace['z'])
        if 'values' in trace:
            trace['values'] = convert_numpy(trace['values'])
        if 'labels' in trace:
            trace['labels'] = convert_numpy(trace['labels'])
    
    layout_dict = fig_dict['layout']
    if 'xaxis' in layout_dict:
        if 'range' in layout_dict['xaxis']:
            layout_dict['xaxis']['range'] = convert_numpy(layout_dict['xaxis']['range'])
    if 'yaxis' in layout_dict:
        if 'range' in layout_dict['yaxis']:
            layout_dict['yaxis']['range'] = convert_numpy(layout_dict['yaxis']['range'])
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{
                margin: 0;
                padding: 20px;
                font-family: Arial, sans-serif;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            #plot {{
                width: 100%;
                height: 100%;
                min-height: 500px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div id="plot"></div>
        </div>
        <script>
            var data = {json.dumps(fig_dict['data'], default=convert_numpy)};
            var layout = {json.dumps(layout_dict, default=convert_numpy)};
            Plotly.newPlot('plot', data, layout);
        </script>
    </body>
    </html>
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

def create_visualizations():
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
        
    df = load_tweets()
    
    layout_config = {
        'template': 'plotly_white',
        'height': 500,
        'margin': dict(l=50, r=50, t=50, b=50),
        'font': dict(family='Arial', size=12)
    }
    
    df['day_of_week'] = df['created_at'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    tweets_by_day = df['day_of_week'].value_counts().reindex(day_order)
    
    df['hour'] = df['created_at'].dt.hour
    tweets_by_hour = df['hour'].value_counts().sort_index()
    
    df['engagement'] = df['retweet_count'] + df['like_count'] + df['reply_count']
    engagement_by_day = df.groupby('day_of_week')['engagement'].mean().reindex(day_order)
    
    engagement_by_hour = df.groupby('hour')['engagement'].mean()
    
    all_topics = []
    for topics in df['main_topics']:
        for topic in topics:
            all_topics.append(topic['topic'])
    
    topic_counts = pd.Series(all_topics).value_counts()
    
    topic_engagement = {}
    for idx, row in df.iterrows():
        for topic in row['main_topics']:
            if topic['topic'] not in topic_engagement:
                topic_engagement[topic['topic']] = []
            topic_engagement[topic['topic']].append(row['engagement'])
    
    topic_avg_engagement = {topic: np.mean(engagements) for topic, engagements in topic_engagement.items()}
    topic_avg_engagement = dict(sorted(topic_avg_engagement.items(), key=lambda x: x[1], reverse=True))
    
    top_15_topics = list(topic_avg_engagement.items())[:15]
    
    dashboard_layout = {
        'template': 'plotly_white',
        'height': 1200,
        'showlegend': False,
        'title': 'Vue d\'ensemble des analyses Twitter',
        'margin': dict(l=50, r=50, t=100, b=50),
        'font': dict(family='Arial', size=12)
    }
    
    fig_dashboard = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            'Distribution des tweets par jour',
            'Distribution des tweets par heure',
            'Engagement moyen par jour',
            'Engagement moyen par heure',
            'Top 15 des sujets principaux',
            'Top 15 des sujets par engagement'
        )
    )
    
    fig_dashboard.add_trace(
        go.Bar(
            x=tweets_by_day.index,
            y=tweets_by_day.values,
            name='Tweets par jour',
            marker_color='#1DA1F2'
        ),
        row=1, col=1
    )
    
    fig_dashboard.add_trace(
        go.Bar(
            x=tweets_by_hour.index,
            y=tweets_by_hour.values,
            name='Tweets par heure',
            marker_color='#17BF63'
        ),
        row=1, col=2
    )
    
    fig_dashboard.add_trace(
        go.Bar(
            x=engagement_by_day.index,
            y=engagement_by_day.values,
            name='Engagement par jour',
            marker_color='#F45D22'
        ),
        row=2, col=1
    )
    
    fig_dashboard.add_trace(
        go.Bar(
            x=engagement_by_hour.index,
            y=engagement_by_hour.values,
            name='Engagement par heure',
            marker_color='#794BC4'
        ),
        row=2, col=2
    )
    
    fig_dashboard.add_trace(
        go.Bar(
            x=topic_counts.index[:15],
            y=topic_counts.values[:15],
            name='Top 15 sujets',
            marker_color='#E0245E'
        ),
        row=3, col=1
    )
    
    fig_dashboard.add_trace(
        go.Bar(
            x=[t[0] for t in top_15_topics],
            y=[t[1] for t in top_15_topics],
            name='Top 15 engagement',
            marker_color='#657786'
        ),
        row=3, col=2
    )
    
    fig_dashboard.update_layout(**dashboard_layout)
    save_plotly_figure(fig_dashboard, 'graphs/dashboard.html')
    
    with open('graphs/stats_report.txt', 'w', encoding='utf-8') as f:
        f.write("Rapport d'analyse des tweets Saegus\n")
        f.write("================================\n\n")
        
        f.write("1. Statistiques générales\n")
        f.write("------------------------\n")
        f.write(f"Nombre total de tweets : {len(df)}\n")
        f.write(f"Période : du {df['created_at'].min().strftime('%Y-%m-%d')} au {df['created_at'].max().strftime('%Y-%m-%d')}\n")
        f.write(f"Engagement total moyen : {df['engagement'].mean():.2f}\n\n")
        
        f.write("2. Distribution par jour\n")
        f.write("------------------------\n")
        for day in day_order:
            count = tweets_by_day.get(day, 0)
            engagement = engagement_by_day.get(day, 0)
            f.write(f"{day}: {count} tweets, engagement moyen: {engagement:.2f}\n")
        f.write("\n")
        
        f.write("3. Top 5 des sujets les plus fréquents\n")
        f.write("------------------------------------\n")
        for topic, count in topic_counts.head().items():
            f.write(f"{topic}: {count} mentions\n")
        f.write("\n")
        
        f.write("4. Top 5 des sujets par engagement\n")
        f.write("--------------------------------\n")
        for topic, engagement in list(topic_avg_engagement.items())[:5]:
            f.write(f"{topic}: {engagement:.2f} d'engagement moyen\n")
        f.write("\n")
        
        f.write("5. Meilleur moment pour tweeter\n")
        f.write("----------------------------\n")
        best_hour = engagement_by_hour.idxmax()
        f.write(f"Heure avec le plus d'engagement : {best_hour}h00 ({engagement_by_hour.max():.2f} d'engagement moyen)\n")
        best_day = engagement_by_day.idxmax()
        f.write(f"Jour avec le plus d'engagement : {best_day} ({engagement_by_day.max():.2f} d'engagement moyen)\n")

if __name__ == "__main__":
    create_visualizations()
    print("Le dashboard a été généré dans le dossier 'graphs'") 