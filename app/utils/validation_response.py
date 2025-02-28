from fastapi import HTTPException
from pydantic import ValidationError

# Function to handle validation erors
def validation_error_response(error: ValidationError):
    errors = []
    for err in error.errors(): # iterrating over each error by err while feching those errors through error.erros()
        errors.append({   # loop chala k har error ka field, messa ge, type extract kiya aur usko error list me append kiya
            'field':'.'.join(map(str, err['loc'])), # Identifies which field has errors ie; age, country, gender...
            'message': err['msg'], # Show validation message. like if age has error, it will show/return'value is not a valid integer'
            'type': err['type'] # Show error type. like if age has error, it will show/return 'value_error.number.not_int_type.
        })

    raise HTTPException(status_code=422, # ye error raise karega aur fastapi response body me dikhayega
                        detail={'errors':errors}) 