const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');
const select = document.getElementById('lista'); // Elemento select de la lista desplegable
const select2 = document.getElementById('listaU'); // Elemento select de la lista desplegable
const continuarBoton = document.getElementById('continuar');

continuarBoton.disabled = true;


const expresiones = {
  numeroCelular: /^\d{7,20}$/, // 7 a 20 numeros.
  numeroTelefono: /^\d{7,20}$/, // 7 a 20 numeros.
  edad: /^[1-9]\d*$/,
  password: /^[a-zA-Z0-9._-]{7,20}$/
};

const campos = {
  numeroCelular: false,
  numeroTelefono: false,
  fecha: false,
  edad: false,
  listaU: false,
  password: false,
  password2: false
};

const validarCampo = (expresion, input, campo) => {
  if (expresion.test(input.value)) {
    document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
    document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
    document.querySelector(`#grupo__${campo} i`).classList.remove('fa-times-circle');
    document.querySelector(`#grupo__${campo} i`).classList.add('fa-check-circle');
    document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo');
    campos[campo] = true;
  } else {
    document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto');
    document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-correcto');
    document.querySelector(`#grupo__${campo} i`).classList.add('fa-times-circle');
    document.querySelector(`#grupo__${campo} i`).classList.remove('fa-check-circle');
    document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.add('formulario__input-error-activo');
    campos[campo] = false;
  }
};

const validarFormulario = (e) => {
	switch (e.target.name) {
	  case 'numeroCelular':
		validarCampo(expresiones.numeroCelular, e.target, 'numeroCelular');
		break;
	  case 'numeroTelefono':
		validarCampo(expresiones.numeroTelefono, e.target, 'numeroTelefono');
		break;
	  case 'edad':
		validarCampo(expresiones.edad, e.target, 'edad');
		break;
	  case 'listaU':
		validarCampo(e.target, 'lista');
		break;
	  case 'password':
		validarCampo(expresiones.password, e.target, 'password');
		validarPassword2();
		break;
	  case 'password2':
		validarPassword2();
		break;
	}
	habilitarBoton();
  };
  

const validarFecha = (input) => {
  const fechaInput = new Date(input.value);
  const fechaActual = new Date();
  if (isNaN(fechaInput) || fechaInput > fechaActual) {
    document.getElementById(`grupo__fecha`).classList.add('formulario__grupo-incorrecto');
    document.getElementById(`grupo__fecha`).classList.remove('formulario__grupo-correcto');
    document.querySelector(`#grupo__fecha i`).classList.add('fa-times-circle');
    document.querySelector(`#grupo__fecha i`).classList.remove('fa-check-circle');
    document.querySelector(`#grupo__fecha .formulario__input-error`).classList.add('formulario__input-error-activo');
    campos.fecha = false;
  } else {
    document.getElementById(`grupo__fecha`).classList.remove('formulario__grupo-incorrecto');
    document.getElementById(`grupo__fecha`).classList.add('formulario__grupo-correcto');
    document.querySelector(`#grupo__fecha i`).classList.remove('fa-times-circle');
    document.querySelector(`#grupo__fecha i`).classList.add('fa-check-circle');
    document.querySelector(`#grupo__fecha .formulario__input-error`).classList.remove('formulario__input-error-activo');
    campos.fecha = true;
  }
};

const validarPassword2 = () => {
	const inputPassword1 = document.getElementById('password');
	const inputPassword2 = document.getElementById('password2');
  
	if (inputPassword1.value !== inputPassword2.value) {
	  document.getElementById(`grupo__password2`).classList.add('formulario__grupo-incorrecto');
	  document.getElementById(`grupo__password2`).classList.remove('formulario__grupo-correcto');
	  document.querySelector(`#grupo__password2 i`).classList.add('fa-times-circle');
	  document.querySelector(`#grupo__password2 i`).classList.remove('fa-check-circle');
	  document.querySelector(`#grupo__password2 .formulario__input-error`).textContent = 'Las contraseñas no coinciden';
	  document.querySelector(`#grupo__password2 .formulario__input-error`).classList.add('formulario__input-error-activo');
	  campos['password2'] = false;
	} else {
	  document.getElementById(`grupo__password2`).classList.remove('formulario__grupo-incorrecto');
	  document.getElementById(`grupo__password2`).classList.add('formulario__grupo-correcto');
	  document.querySelector(`#grupo__password2 i`).classList.remove('fa-times-circle');
	  document.querySelector(`#grupo__password2 i`).classList.add('fa-check-circle');
	  document.querySelector(`#grupo__password2 .formulario__input-error`).classList.remove('formulario__input-error-activo');
	  campos['password2'] = true;
	}
  };
  

  inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
  });

  var enviarDatos = false;
  const terminos = document.getElementById('terminos');
	

  const habilitarBoton = () => {
	if (campos.numeroCelular && campos.numeroTelefono && campos.edad && campos.password && campos.password2 && terminos.checked) {
	  continuarBoton.disabled = false;
	} else {
	  continuarBoton.disabled = true;
	}
  };
  
  // Agregar escuchadores de eventos para los campos
	
	terminos.addEventListener('change', habilitarBoton);
  // Llama a habilitarBoton después de la validación inicial
  habilitarBoton();
  
  // Agregar escuchadores de eventos para los campos
  terminos.addEventListener('change', habilitarBoton);
  
  // Llama a habilitarBoton cada vez que ocurra un evento que pueda cambiar el estado de los campos
  inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
  });