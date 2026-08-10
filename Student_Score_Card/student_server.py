import os

from fastmcp import FastMCP  
from database import get_connection

mcp = FastMCP("Student_MCP_Server")

#tool1 : get student details
@mcp.tool()
def get_student_details(student_id: str):
    """
    return the student_id , Name and class  of a student 
    """
    conn = get_connection()     # connect to sqllite3
    cursor = conn.cursor()      # excecute sql queries
    
    cursor.execute(
            """SELECT name, class FROM students WHERE student_id = ?""", (student_id,)
            )
        
    student = cursor.fetchone()
    conn.close()

    if student:
        return {"student_id": student_id, "student_name": student["name"], "student_class": student["class"]}

    return {"error": "Student not found."}

#tool2 : get student marks
@mcp.tool()
def get_student_marks(student_id: str):
    """
    return the marks of a student
    """
    conn = get_connection()     # connect to sqllite3
    cursor = conn.cursor()      # excecute sql queries

    cursor.execute(
        """SELECT marks FROM students WHERE student_id = ?""", (student_id,)
    )

    student = cursor.fetchone()
    conn.close()

    if student:
        return {"student_id": student_id, "student_marks": student["marks"]}

    return {"error": "Student not found."}

# tool3: chech result pass or fail
@mcp.tool()
def get_student_result(student_id: str):
    """
    return the student result pass or fail based on marks
    passing marks 40 
    """
    conn = get_connection()     # connect to sqllite3
    cursor = conn.cursor()      # excecute sql queries

    cursor.execute(
        """SELECT marks FROM students WHERE student_id = ?""", (student_id,)
    )

    student = cursor.fetchone()
    conn.close()

    if not student:
        return {"error": "Student not found."}

    marks = student["marks"]
    result = "Pass" if marks >= 40 else "Fail"

    return {"student_id": student_id, "student_marks": marks, "result": result}

#tool4: report card

@mcp.tool()
def get_report_card(student_id: str):
    """
    fetch the report card  from file data 
    """
    file_path = f"data/report_card/{student_id}.txt"

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            report_card = f.read()
        return {"student_id": student_id, "report_card": report_card}
    return {"error": "Report card not found."}