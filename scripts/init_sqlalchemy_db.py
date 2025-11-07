import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app
from app.models import db, User


def main():
    app = create_app()
    with app.app_context():
        print("[DB] Creating all tables via SQLAlchemy models...")
        db.create_all()

        # Ensure an admin user exists
        admin = User.query.filter_by(student_id="admin").first()
        if not admin:
            print("[DB] Creating admin user (admin / admin123)...")
            admin = User(
                student_id="admin",
                email="admin@example.com",
                real_name="系统管理员",
                is_admin=True,
                admin_level=2,
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
        else:
            print("[DB] Admin user exists; ensuring password is set.")
            admin.set_password("admin123")
            admin.is_admin = True
            admin.admin_level = 2
            db.session.commit()

        print("[DB] Initialization complete.")


if __name__ == "__main__":
    main()