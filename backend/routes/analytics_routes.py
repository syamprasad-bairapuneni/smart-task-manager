from flask import Blueprint, jsonify
from models import Task, TaskStatus
from utils.auth import token_required
from utils.helpers import (
    calculate_productivity_stats,
    get_weekly_productivity,
    get_most_productive_time,
    calculate_average_completion_time
)

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/stats', methods=['GET'])
@token_required
def get_productivity_stats(current_user_id, **kwargs):
    """Get overall productivity statistics"""
    try:
        tasks = Task.query.filter_by(user_id=current_user_id).all()
        
        stats = calculate_productivity_stats(tasks)
        
        return jsonify({
            'stats': stats
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Failed to get stats: {str(e)}'}), 500


@analytics_bp.route('/weekly', methods=['GET'])
@token_required
def get_weekly_data(current_user_id, **kwargs):
    """Get weekly productivity data"""
    try:
        tasks = Task.query.filter_by(user_id=current_user_id).all()
        
        weekly_data = get_weekly_productivity(tasks)
        
        return jsonify({
            'weekly_data': weekly_data
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Failed to get weekly data: {str(e)}'}), 500


@analytics_bp.route('/productive-time', methods=['GET'])
@token_required
def get_productive_time(current_user_id, **kwargs):
    """Get most productive day and hour analysis"""
    try:
        tasks = Task.query.filter_by(user_id=current_user_id).all()
        
        productive_time = get_most_productive_time(tasks)
        
        return jsonify({
            'productive_time': productive_time
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Failed to get productive time: {str(e)}'}), 500


@analytics_bp.route('/completion-time', methods=['GET'])
@token_required
def get_completion_time(current_user_id, **kwargs):
    """Get average task completion time"""
    try:
        tasks = Task.query.filter_by(user_id=current_user_id).all()
        
        avg_completion = calculate_average_completion_time(tasks)
        
        if not avg_completion:
            return jsonify({
                'message': 'No completed tasks found',
                'completion_time': None
            }), 200
        
        return jsonify({
            'completion_time': avg_completion
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Failed to get completion time: {str(e)}'}), 500


@analytics_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard_data(current_user_id, **kwargs):
    """Get complete dashboard data (all analytics combined)"""
    try:
        tasks = Task.query.filter_by(user_id=current_user_id).all()
        
        stats = calculate_productivity_stats(tasks)
        weekly_data = get_weekly_productivity(tasks)
        productive_time = get_most_productive_time(tasks)
        avg_completion = calculate_average_completion_time(tasks)
        
        # Calculate top categories
        category_counts = stats.get('category_counts', {})
        top_categories = sorted(
            category_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return jsonify({
            'stats': stats,
            'weekly_data': weekly_data,
            'productive_time': productive_time,
            'completion_time': avg_completion,
            'top_categories': [{'category': cat, 'count': count} for cat, count in top_categories]
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Failed to get dashboard data: {str(e)}'}), 500

