#!/usr/bin/env python3
"""
Personal Blog System - Analytics Module
Python script for analyzing blog performance and reader engagement
"""

import json
import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np
import re
from wordcloud import WordCloud
import seaborn as sns

class BlogAnalytics:
    def __init__(self, data_dir=None):
        if data_dir is None:
            # Default path relative to this script
            script_dir = Path(__file__).parent
            self.data_dir = script_dir / '../database'
        else:
            self.data_dir = Path(data_dir)
        
        self.posts_file = self.data_dir / 'posts.json'
        self.categories_file = self.data_dir / 'categories.json'
        self.comments_file = self.data_dir / 'comments.json'
        self.settings_file = self.data_dir / 'settings.json'
        
        self.posts = self.load_data(self.posts_file)
        self.categories = self.load_data(self.categories_file)
        self.comments = self.load_data(self.comments_file)
        self.settings = self.load_data(self.settings_file)
    
    def load_data(self, file_path):
        """Load data from JSON file"""
        try:
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return json.load(f)
            else:
                print(f"Data file not found: {file_path}")
                return []
        except Exception as e:
            print(f"Error loading data from {file_path}: {e}")
            return []
    
    def get_blog_overview(self):
        """Get basic blog statistics"""
        if not self.posts:
            return {
                'total_posts': 0,
                'published_posts': 0,
                'draft_posts': 0,
                'total_views': 0,
                'total_comments': 0,
                'total_likes': 0,
                'average_views_per_post': 0,
                'average_comments_per_post': 0
            }
        
        total_posts = len(self.posts)
        published_posts = len([p for p in self.posts if p.get('published', True)])
        draft_posts = total_posts - published_posts
        total_views = sum(p.get('views', 0) for p in self.posts)
        total_comments = len([c for c in self.comments if c.get('approved', False)])
        total_likes = sum(p.get('likes', 0) for p in self.posts)
        
        avg_views = total_views / published_posts if published_posts > 0 else 0
        avg_comments = total_comments / published_posts if published_posts > 0 else 0
        
        return {
            'total_posts': total_posts,
            'published_posts': published_posts,
            'draft_posts': draft_posts,
            'total_views': total_views,
            'total_comments': total_comments,
            'total_likes': total_likes,
            'average_views_per_post': round(avg_views, 2),
            'average_comments_per_post': round(avg_comments, 2)
        }
    
    def get_content_analysis(self):
        """Analyze content characteristics"""
        if not self.posts:
            return {}
        
        # Word count analysis
        word_counts = []
        reading_times = []
        
        for post in self.posts:
            content = post.get('content', '')
            # Remove HTML tags for word counting
            clean_content = re.sub(r'<[^>]+>', '', content)
            words = len(clean_content.split())
            word_counts.append(words)
            
            # Estimate reading time (average 200 words per minute)
            reading_time = max(1, words // 200)
            reading_times.append(reading_time)
        
        # Tag analysis
        all_tags = []
        for post in self.posts:
            all_tags.extend(post.get('tags', []))
        
        tag_frequency = Counter(all_tags)
        
        # Title length analysis
        title_lengths = [len(post.get('title', '')) for post in self.posts]
        
        return {
            'word_count_stats': {
                'min': min(word_counts) if word_counts else 0,
                'max': max(word_counts) if word_counts else 0,
                'average': round(np.mean(word_counts), 2) if word_counts else 0,
                'median': round(np.median(word_counts), 2) if word_counts else 0
            },
            'reading_time_stats': {
                'min': min(reading_times) if reading_times else 0,
                'max': max(reading_times) if reading_times else 0,
                'average': round(np.mean(reading_times), 2) if reading_times else 0
            },
            'title_length_stats': {
                'min': min(title_lengths) if title_lengths else 0,
                'max': max(title_lengths) if title_lengths else 0,
                'average': round(np.mean(title_lengths), 2) if title_lengths else 0
            },
            'most_used_tags': dict(tag_frequency.most_common(10)),
            'total_unique_tags': len(tag_frequency)
        }
    
    def get_engagement_analysis(self):
        """Analyze reader engagement metrics"""
        if not self.posts:
            return {}
        
        # Engagement rate calculation (comments + likes per view)
        engagement_rates = []
        for post in self.posts:
            views = post.get('views', 0)
            comments = post.get('comments', 0)
            likes = post.get('likes', 0)
            
            if views > 0:
                engagement_rate = ((comments + likes) / views) * 100
                engagement_rates.append(engagement_rate)
        
        # Comment analysis
        comment_lengths = []
        comments_per_day = defaultdict(int)
        
        for comment in self.comments:
            if comment.get('approved', False):
                content = comment.get('content', '')
                comment_lengths.append(len(content))
                
                # Group comments by date
                date = comment.get('date', '').split(' ')[0]  # Get date part only
                if date:
                    comments_per_day[date] += 1
        
        # Find most engaging posts
        engaging_posts = sorted(self.posts, 
                              key=lambda p: p.get('comments', 0) + p.get('likes', 0), 
                              reverse=True)[:5]
        
        return {
            'engagement_rate_stats': {
                'average': round(np.mean(engagement_rates), 2) if engagement_rates else 0,
                'median': round(np.median(engagement_rates), 2) if engagement_rates else 0,
                'max': round(max(engagement_rates), 2) if engagement_rates else 0
            },
            'comment_stats': {
                'total_comments': len(comment_lengths),
                'average_length': round(np.mean(comment_lengths), 2) if comment_lengths else 0,
                'comments_per_day': dict(comments_per_day)
            },
            'most_engaging_posts': [
                {
                    'title': post.get('title', ''),
                    'views': post.get('views', 0),
                    'comments': post.get('comments', 0),
                    'likes': post.get('likes', 0)
                }
                for post in engaging_posts
            ]
        }
    
    def get_category_performance(self):
        """Analyze performance by category"""
        category_stats = defaultdict(lambda: {
            'posts': 0,
            'total_views': 0,
            'total_comments': 0,
            'total_likes': 0,
            'average_views': 0,
            'average_comments': 0,
            'average_likes': 0
        })
        
        for post in self.posts:
            category = post.get('category', 'uncategorized')
            stats = category_stats[category]
            
            stats['posts'] += 1
            stats['total_views'] += post.get('views', 0)
            stats['total_comments'] += post.get('comments', 0)
            stats['total_likes'] += post.get('likes', 0)
        
        # Calculate averages
        for category, stats in category_stats.items():
            if stats['posts'] > 0:
                stats['average_views'] = round(stats['total_views'] / stats['posts'], 2)
                stats['average_comments'] = round(stats['total_comments'] / stats['posts'], 2)
                stats['average_likes'] = round(stats['total_likes'] / stats['posts'], 2)
        
        return dict(category_stats)
    
    def get_temporal_analysis(self):
        """Analyze posting patterns and trends over time"""
        if not self.posts:
            return {}
        
        # Posts by month
        posts_by_month = defaultdict(int)
        views_by_month = defaultdict(int)
        
        # Posts by day of week
        posts_by_weekday = defaultdict(int)
        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for post in self.posts:
            date_str = post.get('date', '')
            if date_str:
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    month_key = date_obj.strftime('%Y-%m')
                    posts_by_month[month_key] += 1
                    views_by_month[month_key] += post.get('views', 0)
                    
                    weekday = weekday_names[date_obj.weekday()]
                    posts_by_weekday[weekday] += 1
                except ValueError:
                    continue
        
        # Publishing frequency
        if posts_by_month:
            months = sorted(posts_by_month.keys())
            if len(months) > 1:
                start_date = datetime.strptime(months[0], '%Y-%m')
                end_date = datetime.strptime(months[-1], '%Y-%m')
                months_diff = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1
                avg_posts_per_month = len(self.posts) / months_diff
            else:
                avg_posts_per_month = len(self.posts)
        else:
            avg_posts_per_month = 0
        
        return {
            'posts_by_month': dict(posts_by_month),
            'views_by_month': dict(views_by_month),
            'posts_by_weekday': dict(posts_by_weekday),
            'average_posts_per_month': round(avg_posts_per_month, 2),
            'most_productive_month': max(posts_by_month.items(), key=lambda x: x[1])[0] if posts_by_month else None,
            'most_productive_weekday': max(posts_by_weekday.items(), key=lambda x: x[1])[0] if posts_by_weekday else None
        }
    
    def get_top_performing_content(self):
        """Get top performing posts by various metrics"""
        if not self.posts:
            return {}
        
        # Sort posts by different metrics
        top_by_views = sorted(self.posts, key=lambda p: p.get('views', 0), reverse=True)[:10]
        top_by_comments = sorted(self.posts, key=lambda p: p.get('comments', 0), reverse=True)[:10]
        top_by_likes = sorted(self.posts, key=lambda p: p.get('likes', 0), reverse=True)[:10]
        
        # Calculate engagement score (weighted combination of metrics)
        for post in self.posts:
            views = post.get('views', 0)
            comments = post.get('comments', 0)
            likes = post.get('likes', 0)
            
            # Weighted engagement score
            engagement_score = views * 1 + comments * 10 + likes * 5
            post['engagement_score'] = engagement_score
        
        top_by_engagement = sorted(self.posts, key=lambda p: p.get('engagement_score', 0), reverse=True)[:10]
        
        return {
            'top_by_views': [
                {
                    'title': post.get('title', ''),
                    'views': post.get('views', 0),
                    'date': post.get('date', ''),
                    'category': post.get('category', '')
                }
                for post in top_by_views
            ],
            'top_by_comments': [
                {
                    'title': post.get('title', ''),
                    'comments': post.get('comments', 0),
                    'date': post.get('date', ''),
                    'category': post.get('category', '')
                }
                for post in top_by_comments
            ],
            'top_by_likes': [
                {
                    'title': post.get('title', ''),
                    'likes': post.get('likes', 0),
                    'date': post.get('date', ''),
                    'category': post.get('category', '')
                }
                for post in top_by_likes
            ],
            'top_by_engagement': [
                {
                    'title': post.get('title', ''),
                    'engagement_score': post.get('engagement_score', 0),
                    'views': post.get('views', 0),
                    'comments': post.get('comments', 0),
                    'likes': post.get('likes', 0),
                    'date': post.get('date', ''),
                    'category': post.get('category', '')
                }
                for post in top_by_engagement
            ]
        }
    
    def get_seo_analysis(self):
        """Analyze SEO-related metrics"""
        if not self.posts:
            return {}
        
        # Title length analysis (optimal: 50-60 characters)
        title_lengths = [len(post.get('title', '')) for post in self.posts]
        optimal_titles = len([l for l in title_lengths if 50 <= l <= 60])
        
        # Meta description analysis (optimal: 150-160 characters)
        meta_desc_lengths = [len(post.get('metaDescription', '')) for post in self.posts]
        optimal_meta_desc = len([l for l in meta_desc_lengths if 150 <= l <= 160])
        
        # Posts with images
        posts_with_images = len([p for p in self.posts if p.get('image')])
        
        # Posts with tags
        posts_with_tags = len([p for p in self.posts if p.get('tags')])
        
        return {
            'title_analysis': {
                'average_length': round(np.mean(title_lengths), 2) if title_lengths else 0,
                'optimal_length_count': optimal_titles,
                'optimal_percentage': round((optimal_titles / len(self.posts)) * 100, 2) if self.posts else 0
            },
            'meta_description_analysis': {
                'average_length': round(np.mean(meta_desc_lengths), 2) if meta_desc_lengths else 0,
                'optimal_length_count': optimal_meta_desc,
                'optimal_percentage': round((optimal_meta_desc / len(self.posts)) * 100, 2) if self.posts else 0
            },
            'content_optimization': {
                'posts_with_images': posts_with_images,
                'posts_with_images_percentage': round((posts_with_images / len(self.posts)) * 100, 2) if self.posts else 0,
                'posts_with_tags': posts_with_tags,
                'posts_with_tags_percentage': round((posts_with_tags / len(self.posts)) * 100, 2) if self.posts else 0
            }
        }
    
    def generate_insights(self):
        """Generate actionable insights based on analytics"""
        insights = []
        
        overview = self.get_blog_overview()
        content_analysis = self.get_content_analysis()
        engagement_analysis = self.get_engagement_analysis()
        category_performance = self.get_category_performance()
        temporal_analysis = self.get_temporal_analysis()
        seo_analysis = self.get_seo_analysis()
        
        # Content insights
        if overview['average_views_per_post'] > 500:
            insights.append("🎉 Excellent! Your posts are getting great visibility with high average views.")
        elif overview['average_views_per_post'] > 100:
            insights.append("👍 Good readership! Consider promoting your content more to increase views.")
        else:
            insights.append("📈 Focus on SEO optimization and content promotion to increase visibility.")
        
        # Engagement insights
        if engagement_analysis.get('engagement_rate_stats', {}).get('average', 0) > 5:
            insights.append("💬 Outstanding engagement! Your readers are actively interacting with your content.")
        elif engagement_analysis.get('engagement_rate_stats', {}).get('average', 0) > 2:
            insights.append("👥 Good engagement levels. Consider adding more call-to-actions to boost interaction.")
        else:
            insights.append("🔄 Low engagement. Try asking questions and encouraging comments at the end of posts.")
        
        # Content length insights
        avg_words = content_analysis.get('word_count_stats', {}).get('average', 0)
        if avg_words > 1500:
            insights.append("📚 Your posts are comprehensive and detailed, which is great for SEO and authority.")
        elif avg_words > 800:
            insights.append("📝 Good post length for readability and SEO. Consider varying length based on topic.")
        else:
            insights.append("📄 Consider writing longer, more detailed posts to improve SEO and provide more value.")
        
        # Category insights
        if category_performance:
            best_category = max(category_performance.items(), key=lambda x: x[1]['average_views'])
            insights.append(f"🏆 '{best_category[0]}' is your top-performing category with {best_category[1]['average_views']:.0f} average views.")
        
        # Publishing frequency insights
        avg_posts_per_month = temporal_analysis.get('average_posts_per_month', 0)
        if avg_posts_per_month >= 4:
            insights.append("📅 Great posting consistency! Regular publishing helps build audience loyalty.")
        elif avg_posts_per_month >= 2:
            insights.append("📆 Good posting frequency. Consider increasing to 3-4 posts per month for better growth.")
        else:
            insights.append("⏰ Increase posting frequency to at least 2-3 posts per month for better engagement.")
        
        # SEO insights
        seo_title_percentage = seo_analysis.get('title_analysis', {}).get('optimal_percentage', 0)
        if seo_title_percentage < 50:
            insights.append("🔍 Optimize your post titles to 50-60 characters for better SEO performance.")
        
        seo_image_percentage = seo_analysis.get('content_optimization', {}).get('posts_with_images_percentage', 0)
        if seo_image_percentage < 80:
            insights.append("🖼️ Add featured images to more posts to improve visual appeal and social sharing.")
        
        return insights
    
    def create_visualizations(self, output_dir=None):
        """Create comprehensive data visualizations"""
        if output_dir is None:
            output_dir = self.data_dir / '../reports'
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(exist_ok=True)
        
        # Set up the plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Create a comprehensive dashboard
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Blog Overview (2x2 grid in top-left)
        ax1 = plt.subplot(3, 4, 1)
        overview = self.get_blog_overview()
        metrics = ['Posts', 'Views', 'Comments', 'Likes']
        values = [overview['published_posts'], overview['total_views'], 
                 overview['total_comments'], overview['total_likes']]
        
        bars = ax1.bar(metrics, values, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'])
        ax1.set_title('Blog Overview', fontweight='bold')
        ax1.set_ylabel('Count')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{value}', ha='center', va='bottom')
        
        # 2. Category Performance
        ax2 = plt.subplot(3, 4, 2)
        category_performance = self.get_category_performance()
        if category_performance:
            categories = list(category_performance.keys())
            avg_views = [stats['average_views'] for stats in category_performance.values()]
            
            ax2.bar(categories, avg_views, color='#9b59b6')
            ax2.set_title('Average Views by Category', fontweight='bold')
            ax2.set_ylabel('Average Views')
            plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
        
        # 3. Engagement Analysis
        ax3 = plt.subplot(3, 4, 3)
        engagement_analysis = self.get_engagement_analysis()
        top_posts = engagement_analysis.get('most_engaging_posts', [])[:5]
        
        if top_posts:
            post_titles = [post['title'][:20] + '...' if len(post['title']) > 20 else post['title'] 
                          for post in top_posts]
            engagement_scores = [post['comments'] + post['likes'] for post in top_posts]
            
            ax3.barh(post_titles, engagement_scores, color='#1abc9c')
            ax3.set_title('Most Engaging Posts', fontweight='bold')
            ax3.set_xlabel('Comments + Likes')
        
        # 4. Publishing Timeline
        ax4 = plt.subplot(3, 4, 4)
        temporal_analysis = self.get_temporal_analysis()
        posts_by_month = temporal_analysis.get('posts_by_month', {})
        
        if posts_by_month:
            months = sorted(posts_by_month.keys())
            post_counts = [posts_by_month[month] for month in months]
            
            ax4.plot(months, post_counts, marker='o', linestyle='-', color='#e67e22')
            ax4.set_title('Publishing Timeline', fontweight='bold')
            ax4.set_ylabel('Posts Published')
            plt.setp(ax4.get_xticklabels(), rotation=45, ha='right')
        
        # 5. Word Count Distribution
        ax5 = plt.subplot(3, 4, 5)
        content_analysis = self.get_content_analysis()
        word_counts = []
        for post in self.posts:
            content = post.get('content', '')
            clean_content = re.sub(r'<[^>]+>', '', content)
            words = len(clean_content.split())
            word_counts.append(words)
        
        if word_counts:
            ax5.hist(word_counts, bins=10, color='#34495e', alpha=0.7)
            ax5.set_title('Word Count Distribution', fontweight='bold')
            ax5.set_xlabel('Word Count')
            ax5.set_ylabel('Number of Posts')
        
        # 6. Tag Cloud (most popular tags)
        ax6 = plt.subplot(3, 4, 6)
        most_used_tags = content_analysis.get('most_used_tags', {})
        
        if most_used_tags:
            tags = list(most_used_tags.keys())[:10]
            counts = list(most_used_tags.values())[:10]
            
            ax6.bar(tags, counts, color='#8e44ad')
            ax6.set_title('Most Popular Tags', fontweight='bold')
            ax6.set_ylabel('Usage Count')
            plt.setp(ax6.get_xticklabels(), rotation=45, ha='right')
        
        # 7. Views vs Engagement Scatter
        ax7 = plt.subplot(3, 4, 7)
        views = [post.get('views', 0) for post in self.posts]
        engagement = [post.get('comments', 0) + post.get('likes', 0) for post in self.posts]
        
        if views and engagement:
            ax7.scatter(views, engagement, alpha=0.6, color='#e74c3c')
            ax7.set_title('Views vs Engagement', fontweight='bold')
            ax7.set_xlabel('Views')
            ax7.set_ylabel('Comments + Likes')
        
        # 8. SEO Optimization Status
        ax8 = plt.subplot(3, 4, 8)
        seo_analysis = self.get_seo_analysis()
        
        seo_metrics = ['Optimal Titles', 'Posts with Images', 'Posts with Tags']
        seo_percentages = [
            seo_analysis.get('title_analysis', {}).get('optimal_percentage', 0),
            seo_analysis.get('content_optimization', {}).get('posts_with_images_percentage', 0),
            seo_analysis.get('content_optimization', {}).get('posts_with_tags_percentage', 0)
        ]
        
        colors = ['#27ae60' if p >= 80 else '#f39c12' if p >= 50 else '#e74c3c' for p in seo_percentages]
        bars = ax8.bar(seo_metrics, seo_percentages, color=colors)
        ax8.set_title('SEO Optimization Status', fontweight='bold')
        ax8.set_ylabel('Percentage (%)')
        ax8.set_ylim(0, 100)
        plt.setp(ax8.get_xticklabels(), rotation=45, ha='right')
        
        # Add percentage labels
        for bar, percentage in zip(bars, seo_percentages):
            height = bar.get_height()
            ax8.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{percentage:.1f}%', ha='center', va='bottom')
        
        # 9. Comments Timeline
        ax9 = plt.subplot(3, 4, 9)
        comments_per_day = engagement_analysis.get('comment_stats', {}).get('comments_per_day', {})
        
        if comments_per_day:
            dates = sorted(comments_per_day.keys())[-30:]  # Last 30 days
            comment_counts = [comments_per_day.get(date, 0) for date in dates]
            
            ax9.plot(dates, comment_counts, marker='o', linestyle='-', color='#2ecc71')
            ax9.set_title('Comments Timeline (Last 30 Days)', fontweight='bold')
            ax9.set_ylabel('Comments')
            plt.setp(ax9.get_xticklabels(), rotation=45, ha='right')
        
        # 10. Publishing Day of Week
        ax10 = plt.subplot(3, 4, 10)
        posts_by_weekday = temporal_analysis.get('posts_by_weekday', {})
        
        if posts_by_weekday:
            weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            weekday_counts = [posts_by_weekday.get(day, 0) for day in weekdays]
            
            ax10.bar(weekdays, weekday_counts, color='#f39c12')
            ax10.set_title('Posts by Day of Week', fontweight='bold')
            ax10.set_ylabel('Number of Posts')
            plt.setp(ax10.get_xticklabels(), rotation=45, ha='right')
        
        # 11. Content Performance Heatmap
        ax11 = plt.subplot(3, 4, (11, 12))
        
        # Create a performance matrix
        categories = list(set(post.get('category', 'uncategorized') for post in self.posts))
        metrics = ['Views', 'Comments', 'Likes']
        
        performance_matrix = []
        for category in categories:
            category_posts = [p for p in self.posts if p.get('category') == category]
            if category_posts:
                avg_views = np.mean([p.get('views', 0) for p in category_posts])
                avg_comments = np.mean([p.get('comments', 0) for p in category_posts])
                avg_likes = np.mean([p.get('likes', 0) for p in category_posts])
                performance_matrix.append([avg_views, avg_comments, avg_likes])
            else:
                performance_matrix.append([0, 0, 0])
        
        if performance_matrix:
            im = ax11.imshow(performance_matrix, cmap='YlOrRd', aspect='auto')
            ax11.set_xticks(range(len(metrics)))
            ax11.set_xticklabels(metrics)
            ax11.set_yticks(range(len(categories)))
            ax11.set_yticklabels(categories)
            ax11.set_title('Category Performance Heatmap', fontweight='bold')
            
            # Add colorbar
            plt.colorbar(im, ax=ax11, shrink=0.8)
        
        plt.tight_layout()
        
        # Save the comprehensive dashboard
        output_file = output_dir / 'blog_analytics_dashboard.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Analytics dashboard saved to: {output_file}")
        
        plt.close()
        
        # Create word cloud if there are enough posts
        if len(self.posts) > 0:
            self.create_word_cloud(output_dir)
    
    def create_word_cloud(self, output_dir):
        """Create a word cloud from blog content"""
        try:
            # Combine all post content
            all_text = ""
            for post in self.posts:
                title = post.get('title', '')
                content = post.get('content', '')
                tags = ' '.join(post.get('tags', []))
                
                # Remove HTML tags
                clean_content = re.sub(r'<[^>]+>', '', content)
                all_text += f" {title} {clean_content} {tags}"
            
            if all_text.strip():
                # Create word cloud
                wordcloud = WordCloud(
                    width=800, 
                    height=400, 
                    background_color='white',
                    colormap='viridis',
                    max_words=100
                ).generate(all_text)
                
                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                plt.title('Blog Content Word Cloud', fontsize=16, fontweight='bold')
                
                output_file = output_dir / 'blog_wordcloud.png'
                plt.savefig(output_file, dpi=300, bbox_inches='tight')
                print(f"Word cloud saved to: {output_file}")
                plt.close()
                
        except ImportError:
            print("WordCloud library not available. Skipping word cloud generation.")
        except Exception as e:
            print(f"Error creating word cloud: {e}")
    
    def generate_report(self, output_file=None):
        """Generate a comprehensive analytics report"""
        overview = self.get_blog_overview()
        content_analysis = self.get_content_analysis()
        engagement_analysis = self.get_engagement_analysis()
        category_performance = self.get_category_performance()
        temporal_analysis = self.get_temporal_analysis()
        top_content = self.get_top_performing_content()
        seo_analysis = self.get_seo_analysis()
        insights = self.generate_insights()
        
        report = f"""
# Blog Analytics Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- **Total Posts:** {overview['total_posts']} ({overview['published_posts']} published, {overview['draft_posts']} drafts)
- **Total Views:** {overview['total_views']:,}
- **Total Comments:** {overview['total_comments']}
- **Total Likes:** {overview['total_likes']}
- **Average Views per Post:** {overview['average_views_per_post']}
- **Average Comments per Post:** {overview['average_comments_per_post']}

## Content Analysis

### Word Count Statistics
- **Average Words per Post:** {content_analysis.get('word_count_stats', {}).get('average', 0)}
- **Shortest Post:** {content_analysis.get('word_count_stats', {}).get('min', 0)} words
- **Longest Post:** {content_analysis.get('word_count_stats', {}).get('max', 0)} words
- **Median Length:** {content_analysis.get('word_count_stats', {}).get('median', 0)} words

### Reading Time
- **Average Reading Time:** {content_analysis.get('reading_time_stats', {}).get('average', 0)} minutes
- **Range:** {content_analysis.get('reading_time_stats', {}).get('min', 0)}-{content_analysis.get('reading_time_stats', {}).get('max', 0)} minutes

### Tags and Topics
- **Total Unique Tags:** {content_analysis.get('total_unique_tags', 0)}
- **Most Popular Tags:**
"""
        
        most_used_tags = content_analysis.get('most_used_tags', {})
        for tag, count in list(most_used_tags.items())[:10]:
            report += f"  - {tag}: {count} posts\n"
        
        report += f"""
## Engagement Analysis

### Overall Engagement
- **Average Engagement Rate:** {engagement_analysis.get('engagement_rate_stats', {}).get('average', 0):.2f}%
- **Median Engagement Rate:** {engagement_analysis.get('engagement_rate_stats', {}).get('median', 0):.2f}%
- **Best Engagement Rate:** {engagement_analysis.get('engagement_rate_stats', {}).get('max', 0):.2f}%

### Comment Statistics
- **Total Approved Comments:** {engagement_analysis.get('comment_stats', {}).get('total_comments', 0)}
- **Average Comment Length:** {engagement_analysis.get('comment_stats', {}).get('average_length', 0)} characters

### Most Engaging Posts
"""
        
        for i, post in enumerate(engagement_analysis.get('most_engaging_posts', [])[:5], 1):
            report += f"{i}. **{post['title']}** - {post['views']} views, {post['comments']} comments, {post['likes']} likes\n"
        
        report += f"""
## Category Performance
"""
        
        for category, stats in category_performance.items():
            report += f"""
### {category.title()}
- **Posts:** {stats['posts']}
- **Total Views:** {stats['total_views']:,}
- **Average Views:** {stats['average_views']:.1f}
- **Total Comments:** {stats['total_comments']}
- **Average Comments:** {stats['average_comments']:.1f}
- **Total Likes:** {stats['total_likes']}
- **Average Likes:** {stats['average_likes']:.1f}
"""
        
        report += f"""
## Publishing Patterns

### Frequency
- **Average Posts per Month:** {temporal_analysis.get('average_posts_per_month', 0):.1f}
- **Most Productive Month:** {temporal_analysis.get('most_productive_month', 'N/A')}
- **Most Productive Day:** {temporal_analysis.get('most_productive_weekday', 'N/A')}

### Posts by Day of Week
"""
        
        posts_by_weekday = temporal_analysis.get('posts_by_weekday', {})
        for day, count in posts_by_weekday.items():
            report += f"- {day}: {count} posts\n"
        
        report += f"""
## Top Performing Content

### Most Viewed Posts
"""
        
        for i, post in enumerate(top_content.get('top_by_views', [])[:5], 1):
            report += f"{i}. **{post['title']}** - {post['views']:,} views ({post['date']})\n"
        
        report += f"""
### Most Commented Posts
"""
        
        for i, post in enumerate(top_content.get('top_by_comments', [])[:5], 1):
            report += f"{i}. **{post['title']}** - {post['comments']} comments ({post['date']})\n"
        
        report += f"""
### Highest Engagement Score
"""
        
        for i, post in enumerate(top_content.get('top_by_engagement', [])[:5], 1):
            report += f"{i}. **{post['title']}** - Score: {post['engagement_score']} ({post['views']} views, {post['comments']} comments, {post['likes']} likes)\n"
        
        report += f"""
## SEO Analysis

### Title Optimization
- **Average Title Length:** {seo_analysis.get('title_analysis', {}).get('average_length', 0):.1f} characters
- **Optimal Length Titles (50-60 chars):** {seo_analysis.get('title_analysis', {}).get('optimal_length_count', 0)} ({seo_analysis.get('title_analysis', {}).get('optimal_percentage', 0):.1f}%)

### Meta Description Optimization
- **Average Meta Description Length:** {seo_analysis.get('meta_description_analysis', {}).get('average_length', 0):.1f} characters
- **Optimal Length Descriptions (150-160 chars):** {seo_analysis.get('meta_description_analysis', {}).get('optimal_length_count', 0)} ({seo_analysis.get('meta_description_analysis', {}).get('optimal_percentage', 0):.1f}%)

### Content Optimization
- **Posts with Featured Images:** {seo_analysis.get('content_optimization', {}).get('posts_with_images', 0)} ({seo_analysis.get('content_optimization', {}).get('posts_with_images_percentage', 0):.1f}%)
- **Posts with Tags:** {seo_analysis.get('content_optimization', {}).get('posts_with_tags', 0)} ({seo_analysis.get('content_optimization', {}).get('posts_with_tags_percentage', 0):.1f}%)

## Key Insights and Recommendations
"""
        
        for insight in insights:
            report += f"- {insight}\n"
        
        report += f"""
## Recommendations for Growth

### Content Strategy
1. **Consistency:** Maintain regular publishing schedule (aim for 3-4 posts per month)
2. **Length:** Target 1000-2000 words per post for better SEO performance
3. **Engagement:** End posts with questions to encourage comments
4. **Visuals:** Include featured images in all posts

### SEO Optimization
1. **Titles:** Keep titles between 50-60 characters for optimal search display
2. **Meta Descriptions:** Write compelling 150-160 character descriptions
3. **Tags:** Use 3-5 relevant tags per post
4. **Internal Linking:** Link between related posts to improve site structure

### Audience Engagement
1. **Comments:** Respond to comments promptly to encourage discussion
2. **Social Media:** Share posts across social platforms
3. **Email:** Build an email list for direct reader communication
4. **Community:** Engage with other bloggers in your niche

### Analytics Tracking
1. **Monitor:** Track these metrics monthly to identify trends
2. **A/B Test:** Experiment with different post formats and topics
3. **User Feedback:** Survey readers about content preferences
4. **Performance:** Focus on replicating successful content patterns

---
*Report generated by Blog Analytics System*
"""
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {output_file}")
        else:
            print(report)
        
        return report
    
    def export_to_csv(self, output_dir=None):
        """Export data to CSV files for external analysis"""
        if output_dir is None:
            output_dir = self.data_dir / '../reports'
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(exist_ok=True)
        
        # Export posts
        if self.posts:
            df_posts = pd.DataFrame(self.posts)
            posts_file = output_dir / 'blog_posts_export.csv'
            df_posts.to_csv(posts_file, index=False)
            print(f"Posts exported to: {posts_file}")
        
        # Export comments
        if self.comments:
            df_comments = pd.DataFrame(self.comments)
            comments_file = output_dir / 'blog_comments_export.csv'
            df_comments.to_csv(comments_file, index=False)
            print(f"Comments exported to: {comments_file}")
        
        # Export categories
        if self.categories:
            df_categories = pd.DataFrame(self.categories)
            categories_file = output_dir / 'blog_categories_export.csv'
            df_categories.to_csv(categories_file, index=False)
            print(f"Categories exported to: {categories_file}")

def main():
    """Main function for command-line usage"""
    analytics = BlogAnalytics()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'report':
            output_file = sys.argv[2] if len(sys.argv) > 2 else None
            analytics.generate_report(output_file)
        
        elif command == 'visualize':
            output_dir = sys.argv[2] if len(sys.argv) > 2 else None
            analytics.create_visualizations(output_dir)
        
        elif command == 'export':
            output_dir = sys.argv[2] if len(sys.argv) > 2 else None
            analytics.export_to_csv(output_dir)
        
        elif command == 'insights':
            insights = analytics.generate_insights()
            print("Blog Insights:")
            print("=" * 20)
            for insight in insights:
                print(f"  {insight}")
        
        elif command == 'overview':
            overview = analytics.get_blog_overview()
            print("Blog Overview:")
            print("=" * 20)
            for key, value in overview.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
        
        else:
            print("Unknown command. Available commands: report, visualize, export, insights, overview")
    
    else:
        # Default: show overview and insights
        print("Personal Blog Analytics")
        print("=" * 25)
        overview = analytics.get_blog_overview()
        for key, value in overview.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        print("\nKey Insights:")
        insights = analytics.generate_insights()
        for insight in insights:
            print(f"  {insight}")

if __name__ == "__main__":
    main()

