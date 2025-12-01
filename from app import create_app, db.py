from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User(
        student_id='admin',
        email='admin@example.com',
        real_name='系统管理员',
        is_admin=True,
        admin_level=3
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print('管理员创建成功')