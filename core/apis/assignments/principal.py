from flask import Blueprint
from core import db
from core.models.assignments import Assignment, Teacher
from core.apis import decorators
from core.apis.assignments.schema import AssignmentSchema, AssignmentGradeSchema, TeachersSchema
from core.apis.responses import APIResponse


principal_assignments_resources=Blueprint('principal_assignments_resources',__name__)


@principal_assignments_resources.route('/teachers', methods=['GET'],  strict_slashes=False)
@decorators.authenticate_principal
def all_teachers(p):
    """Return list of all teachers"""
    all_teachers=Teacher.get_all_teachers()
    data=TeachersSchema().dump(all_teachers, many=True)
    return APIResponse.respond(data=data)

@principal_assignments_resources.route('/assignments', methods=['GET'],  strict_slashes=False)
@decorators.authenticate_principal
def all_assignments(p):
    """Return list of all assignments"""
    assignment=Assignment.get_submitted_or_graded_assignments()
    data=AssignmentSchema().dump(assignment, many=True)
    return APIResponse.respond(data=data)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'],  strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_an_assignment(p,incoming_payload):
    """Grade or re-grade an assignment"""
    assignment=AssignmentGradeSchema().load(incoming_payload)
    ass=Assignment.update_grade(id=assignment.id,grade=assignment.grade)
    db.session.commit()
    data=AssignmentSchema().dump(ass)
    return APIResponse.respond(data=data)