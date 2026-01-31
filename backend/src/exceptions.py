class TaskNotFoundException(Exception):
    """Raised when a task is not found"""
    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class UnauthorizedAccessException(Exception):
    """Raised when a user tries to access a task they don't own"""
    def __init__(self, user_id, task_id):
        self.user_id = user_id
        self.task_id = task_id
        super().__init__(f"User {user_id} does not have access to task {task_id}")