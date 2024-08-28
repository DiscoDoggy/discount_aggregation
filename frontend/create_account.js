let email_input = document.getElementById("email-input");
let pwd_input = document.getElementById("password-input");
let confirm_pwd_input = document.getElementById("confirm-password-input");

pwd_input.addEventListener("input", ()=> {
    let uppercase_req = false;
    let digit_req = false;
    let special_char_req = false;

    if(pwd_input.validity.tooShort)
    {
        pwd_input.setCustomValidity("Should be at least 8 characters long!");
    }

    else
    {
    
        for(let i = 0; i < pwd_input.textContent.length; i++)
        {
            const pwd_char = pwd_input.textContent[i];
            if(pwd_char === pwd_char.toUpperCase())
            {
                uppercase_req = true;
            }
            else if(parseInt(pwd_char) != NaN)
            {
                digit_req = true;
            }
        }

        const special_char_re = /[^a-zA-Z0-9]/;
        if(special_char_re.test(pwd_input.textContent))
        {
            special_char_req = true;
        }

        if(upper_case_req && digit_req && special_char_req)
        {
            pwd_input.setCustomValidity("");
        }
        else if(!uppercase_req)
        {
            pwd_input.setCustomValidity("Password should contain at least one uppercase letter");
        }
        else if(!digit_req)
        {
            pwd_input.setCustomValidity("Password should contain at least one digit");
        }
        else if (!special_char_req)
        {
            pwd_input.setCustomValidity("Password should contain at least one special character");
        }
        else
        {
            throw new Error("In create_account.js...Password case not accounted for");
        }
    }

});

confirm_pwd_input.addEventListener("blur", ()=>{
    if(confirm_pwd_input.textContent != pwd_input.textContent)
    {
        confirm_pwd_input.setCustomValidity("Password and confirm password do not match");
    }
});