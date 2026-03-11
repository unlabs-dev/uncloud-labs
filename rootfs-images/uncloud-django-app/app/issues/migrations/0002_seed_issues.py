from django.db import migrations


def seed_issues(apps, schema_editor):
    Issue = apps.get_model("issues", "Issue")
    Issue.objects.create(
        title="Fix login page error on mobile",
        description="Users on mobile devices are seeing a 500 error when submitting the login form.",
        status="OPEN",
        priority=3,
    )
    Issue.objects.create(
        title="Add pagination to issue list",
        description="The issue list page loads all issues at once. Add pagination to improve performance.",
        status="IN_PROGRESS",
        priority=2,
    )


def unseed_issues(apps, schema_editor):
    Issue = apps.get_model("issues", "Issue")
    Issue.objects.filter(
        title__in=[
            "Fix login page error on mobile",
            "Add pagination to issue list",
        ]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("issues", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_issues, reverse_code=unseed_issues),
    ]
