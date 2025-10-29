from datetime import datetime, timedelta
from collections import defaultdict


def calculate_productivity_stats(tasks):
    """Calculate productivity statistics from tasks"""
    total_tasks = len(tasks)
    completed_tasks = [t for t in tasks if t.status.value == 'Completed']
    pending_tasks = [t for t in tasks if t.status.value == 'Pending']
    
    completion_rate = (len(completed_tasks) / total_tasks * 100) if total_tasks > 0 else 0
    
    # Count by category
    category_counts = defaultdict(int)
    for task in tasks:
        if task.category:
            category_counts[task.category] += 1
    
    # Count by priority
    priority_counts = defaultdict(int)
    for task in tasks:
        priority_counts[task.priority.value] += 1
    
    return {
        'total_tasks': total_tasks,
        'completed_tasks': len(completed_tasks),
        'pending_tasks': len(pending_tasks),
        'completion_rate': round(completion_rate, 2),
        'category_counts': dict(category_counts),
        'priority_counts': dict(priority_counts)
    }


def get_weekly_productivity(tasks):
    """Get productivity data for the last 7 days"""
    today = datetime.now().date()
    week_data = []
    
    for i in range(6, -1, -1):  # Last 7 days
        date = today - timedelta(days=i)
        date_str = date.isoformat()
        
        day_tasks = [t for t in tasks if t.created_at.date() == date]
        # Completed counted by completion date if available, else created date
        completed = len([
            t for t in tasks
            if t.status.value == 'Completed' and (
                (t.completed_at and t.completed_at.date() == date) or
                (not t.completed_at and t.created_at.date() == date)
            )
        ])
        pending = len([t for t in day_tasks if t.status.value == 'Pending'])
        
        week_data.append({
            'date': date_str,
            'completed': completed,
            'pending': pending,
            'total': len(day_tasks)
        })
    
    return week_data


def get_most_productive_time(tasks):
    """Analyze tasks to find most productive day and hour"""
    day_counts = defaultdict(int)
    hour_counts = defaultdict(int)
    
    for task in tasks:
        if task.status.value == 'Completed':
            reference_dt = task.completed_at or task.updated_at or task.created_at
            # Get day of week
            day_name = reference_dt.strftime('%A')
            day_counts[day_name] += 1
            # Get hour of day
            hour = reference_dt.hour
            hour_counts[hour] += 1
    
    most_productive_day = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else None
    most_productive_hour = max(hour_counts.items(), key=lambda x: x[1])[0] if hour_counts else None
    
    return {
        'most_productive_day': most_productive_day,
        'most_productive_hour': most_productive_hour,
        'day_distribution': dict(day_counts),
        'hour_distribution': dict(hour_counts)
    }


def calculate_average_completion_time(tasks):
    """Calculate average time to complete tasks"""
    completed_tasks = [t for t in tasks if t.status.value == 'Completed']
    
    if not completed_tasks:
        return None
    
    total_time = timedelta(0)
    valid_count = 0
    
    for task in completed_tasks:
        reference_completion = task.completed_at or task.updated_at
        if reference_completion and task.created_at:
            time_diff = reference_completion - task.created_at
            # Only count tasks completed within 30 days
            if time_diff.days < 30:
                total_time += time_diff
                valid_count += 1
    
    if valid_count == 0:
        return None
    
    avg_time = total_time / valid_count
    return {
        'average_hours': round(avg_time.total_seconds() / 3600, 2),
        'average_days': round(avg_time.days, 2),
        'sample_size': valid_count
    }

