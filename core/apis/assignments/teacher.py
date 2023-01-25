from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema
teacher_grading_resources = Blueprint('teacher_grading_resources', __name__)


@teacher_grading_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments"""
    students_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)



@teacher_grading_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

    gradeded_assignment = Assignment.grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        principal=p
    )
    db.session.commit()
    gradeded_assignment_dump = AssignmentSchema().dump(gradeded_assignment)
    return APIResponse.respond(data=gradeded_assignment_dump)
