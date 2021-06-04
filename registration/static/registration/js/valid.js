var selector = document.querySelector("input[type='tel']")
var im = Inputmask("+7(999)-999-99-99")
im.mask(selector)

new JustValidate(".regist__form", {
    rules: {
        name: {
            required: true,
            minLength: 3,
            maxLength: 15,
        },
        phone: {
            required: true,
            function: (name, value) => {
                const phone = selector.inputmask.unmaskedvalue()

                return Number(phone) && phone.length === 10
            }
        },
        password1: {
            required: true,
            minLength: 6,
        },
        password2: {
            function: (name, value) => {
                const pass1 = $('#password_1').val()
                const pass2 = $('#password_2').val()
                return (pass2 === pass1)

            }
        }


    },
    message: {
        password2: {
            error: 'dldldld'
        }
    }


})