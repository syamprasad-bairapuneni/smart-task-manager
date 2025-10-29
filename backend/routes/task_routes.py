from flask import Blueprint, request, jsonify
from models import db, Task, TaskStatus, TaskPriority
from utils.auth import token_required
from datetime import datetime

task_bp = Blueprint('tasks', __name__)


@task_bp.route('/', methods=['GET'])
@token_required
def get_tasks(current_user_id, **kwargs):
    """Get all tasks for the current user with filtering"""
    try:
        # Get query parameters
        status = request.args.get('status')
        category = request.args.get('category')
        priority = request.args.get('priority')
        search = request.args.get('search')
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Base query
        query = Task.query.filter_by(user_id=current_user_id)
        
        # Apply filters
        if status:
            try:
                task_status = TaskStatus(status)
                query = query.filter_by(status=task_status)
            except ValueError:
                pass
        
        if category:
            query = query.filter_by(category=category)
        
        if priority:
            try:
                task_priority = TaskPriority(priority)
                query = query.filter_by(priority=task_priority)
            except ValueError:
                pass
        
        if search:
            search_term = f'%{search}%'
            query = query.filter(
                db.or_(
                    Task.title.like(search_term),
                    Task.description.like(search_term)
                )
            )
        
        # Apply sorting
        if hasattr(Task, sort_by):
            sort_column = getattr(Task, sort_by)
            if sort_order.lower() == 'asc':
                query = query.order_by(sort_column.asc())
            else:
                query = query.order_by(sort_column.desc())
        
        tasks = query.all()
        
        return jsonify({
            'tasks': [task.to_dict() for task in tasks],
            'count': len(tasks)
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Failed to get tasks: {str(e)}'}), 500


@task_bp.route('/<int:task_id>', methods=['GET'])
@token_required
def get_task(task_id, current_user_id, **kwargs):
    """Get a specific task by ID"""
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
        
        if not task:
            return jsonify({'message': 'Task not found'}), 404
        
        return jsonify({
            'task': task.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Failed to get task: {str(e)}'}), 500


@task_bp.route('/', methods=['POST'])
@token_required
def create_task(current_user_id, **kwargs):
    """Create a new task"""
    try:
        data = request.get_json()
        
        if not data or not data.get('title'):
            return jsonify({'message': 'Title is required'}), 400
        
        # Parse deadline if provided
        deadline = None
        if data.get('deadline'):
            try:
                deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Parse priority
        priority = TaskPriority.MEDIUM
        if data.get('priority'):
            try:
                priority = TaskPriority(data['priority'])
            except ValueError:
                pass
        
        # Create task
        task = Task(
            user_id=current_user_id,
            title=data['title'].strip(),
            description=data.get('description', '').strip(),
            category=data.get('category', '').strip() if data.get('category') else None,
            priority=priority,
            deadline=deadline,
            status=TaskStatus.PENDING
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'message': 'Task created successfully',
            'task': task.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to create task: {str(e)}'}), 500


@task_bp.route('/<int:task_id>', methods=['PUT'])
@token_required
def update_task(task_id, current_user_id, **kwargs):
    """Update an existing task"""
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
        
        if not task:
            return jsonify({'message': 'Task not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if data.get('title'):
            task.title = data['title'].strip()
        
        if 'description' in data:
            task.description = data['description'].strip() if data['description'] else ''
        
        if 'category' in data:
            task.category = data['category'].strip() if data.get('category') else None
        
        if data.get('priority'):
            try:
                task.priority = TaskPriority(data['priority'])
            except ValueError:
                pass
        
        if data.get('deadline'):
            try:
                task.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        if data.get('status'):
            try:
                new_status = TaskStatus(data['status'])
                # Set/clear completion timestamp when status changes
                if task.status != new_status:
                    task.status = new_status
                    if new_status == TaskStatus.COMPLETED:
                        task.completed_at = datetime.utcnow()
                    else:
                        task.completed_at = None
            except ValueError:
                pass
        
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Task updated successfully',
            'task': task.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update task: {str(e)}'}), 500


@task_bp.route('/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(task_id, current_user_id, **kwargs):
    """Delete a task"""
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
        
        if not task:
            return jsonify({'message': 'Task not found'}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({
            'message': 'Task deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to delete task: {str(e)}'}), 500


@task_bp.route('/<int:task_id>/complete', methods=['PUT'])
@token_required
def toggle_task_complete(task_id, current_user_id, **kwargs):
    """Toggle task completion status"""
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
        
        if not task:
            return jsonify({'message': 'Task not found'}), 404
        
        # Toggle status and manage completed_at
        if task.status == TaskStatus.PENDING:
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
        else:
            task.status = TaskStatus.PENDING
            task.completed_at = None
        
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Task status updated successfully',
            'task': task.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update task status: {str(e)}'}), 500

