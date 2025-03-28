from models import db,TestCases
import json

def save_tests():
    TestCases.query.delete()
    db.session.commit()

    # create test cases
    save_input(1, 6, 1, 2, 3)
    save_input(1, 14, 5, 5, 4)
    save_input(1, 60, 30, 20, 10) 
    save_input(2, 25, 5)     
    save_input(2, 100, 10)
    save_input(2, 225, 15)
    save_input(3, 10, "hi", "my", 6)     
    save_input(3, 15, "hello", 4, "python")
    save_input(3, 20, 9, "world", "python")

    output_tests()


def save_input(progassignment_id, output, *args):
    data_json = json.dumps(args)  # Convert *args to a JSON string
    new_test = TestCases(progassignment_id=progassignment_id, input=data_json, output=output)
    db.session.add(new_test)
    db.session.commit()


def output_tests():
    tests = TestCases.query.all()
    for test in tests:
        input = json.loads(test.input)
        # print(input)
        
        try:
            output = json.loads(test.output)
        except:
            output = test.output

        # print(output)
        print(f"code_output = solution({', '.join(repr(arg) for arg in input)})")