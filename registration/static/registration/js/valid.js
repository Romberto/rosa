  document.addEventListener("DOMContentLoaded", () => {
     var selector = $('#id_phone')
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

            var phon = document.getElementById('id_phone')
            phone = phon.inputmask.unmaskedvalue()
                return Number(phone) && phone.length === 10
            }
        },
        password1: {
            required: true,
            minLength: 6,
        },
        password2:{
            required:true,
            function:(name, value) =>{
                pass1 = document.getElementById('id_password').value
                pass2 = document.getElementById('id_password2').value

                return pass1 === pass2
            }
        }
    }
})
  });


