const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');
const select = document.getElementById('lista'); // Elemento select de la lista desplegable
const select2 = document.getElementById('listaU'); // Elemento select de la lista desplegable
const lista = document.getElementById('listaU');
const otroCampo = document.getElementById('otro-campo');
const otroTexto = document.getElementById('otro_texto');
const continuarBoton = document.getElementById('continuar');


const expresiones = {
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
	apellido: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
	numero: /^\d{7,20}$/, // 7 a 20 numeros.
	numeroCelular: /^\d{7,20}$/, // 7 a 20 numeros.
	numeroTelefono: /^\d{7,20}$/, // 7 a 20 numeros.
	edad: /^[1-9]\d*$/,
	listaU: /^[^0]$/,
	otro_texto: /^[a-zA-ZÀ-ÿ\s]{1,40}$/,
	password: /^[a-zA-Z0-9._-]{7,20}$/ 
	
}

const campos = {
	nombre: false,
	apellido: false,
	lista: false,
	numero: false,
	numeroCelular: false,
	numeroTelefono: false,
	fecha: false,
	edad: false,
	listaU: false,
	otro_texto: false,
	password: false,
	password2: false
	
}

const validarFormulario = (e) => {
	switch (e.target.name) {
		case "nombre":
			validarCampo(expresiones.nombre, e.target, 'nombre');
			break;
		case "apellido":
			validarCampo(expresiones.apellido, e.target, 'apellido');
			break;
		case "lista":
			validarCampo(null, select, 'lista');
			break;
		case "numero":
			validarCampo(expresiones.numero, e.target, 'numero');
		break;
		case "numeroCelular":
			validarCampo(expresiones.numeroCelular, e.target, 'numeroCelular');
		break;
		case "numeroTelefono":
			validarCampo(expresiones.numeroTelefono, e.target, 'numeroTelefono');
		break;
		case "fecha":
			validarFecha(e.target);
			break;
		case "edad":
			validarCampo(expresiones.edad, e.target, 'edad');
			break;
		case "listaU":
			validarCampo(null, select2, 'listaU');
			campos.listaU = true;
			break;
		case "otro_texto":
			validarCampo(expresiones.otro_texto, e.target, 'otro_texto');
			break;		
		case "password":
			validarCampo(expresiones.password, e.target, 'password');
		break;
		case "password2":
			validarPassword2();
		break;  
}
}



lista.addEventListener('change', () => {
	if (lista.value === 'otro') {
	  otroCampo.style.display = 'block';
	  otroTexto.required = true;
	} else {
	  otroCampo.style.display = 'none';
	  otroTexto.required = false;
	}
  });

select2.addEventListener('change', validarFormulario);
select.addEventListener('change', validarFormulario);
lista.addEventListener('change', validarFormulario);
otroCampo.addEventListener('change', validarFormulario);
otroTexto.addEventListener('change', validarFormulario)

const validarCampo = (expresion, input, campo) => {
	if (expresion && expresion.test(input.value)) {
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-check-circle');
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-times-circle');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo');
		campos[campo] = true;
	} else if (!expresion && input.selectedIndex !== 0 && input.options[input.selectedIndex].value !== "") { 
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-check-circle');
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-times-circle');
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
}

const validarFecha = (input) => {
	const fechaInput = new Date(input.value);
	const fechaActual = new Date();
	if (fechaInput.toString() === 'Invalid Date') {
	  document.getElementById(`grupo__fecha`).classList.add('formulario__grupo-incorrecto');
	  document.getElementById(`grupo__fecha`).classList.remove('formulario__grupo-correcto');
	  document.querySelector(`#grupo__fecha i`).classList.add('fa-times-circle');
	  document.querySelector(`#grupo__fecha i`).classList.remove('fa-check-circle');
	  document.querySelector(`#grupo__fecha .formulario__input-error`).classList.add('formulario__input-error-activo');
	  campos.fecha = false;
	} else if (fechaInput > fechaActual) {
	  document.getElementById(`grupo__fecha`).classList.add('formulario__grupo-incorrecto');
	  document.getElementById(`grupo__fecha`).classList.remove('formulario__grupo-correcto');
	  document.querySelector(`#grupo__fecha i`).classList.add('fa-times-circle');
	  document.querySelector(`#grupo__fecha i`).classList.remove('fa-check-circle');
	  document.querySelector(`#grupo__fecha .formulario__input-error`).textContent = 'La fecha debe ser anterior a la fecha actual';
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
  }
  
  const validarPassword2 = () => {
	const inputPassword1 = document.getElementById('password');
	const inputPassword2 = document.getElementById('password2');

	if(inputPassword1.value !== inputPassword2.value && inputPassword2.value !== ''){
		document.getElementById(`grupo__password2`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`grupo__password2`).classList.remove('formulario__grupo-correcto');
		document.querySelector(`#grupo__password2 i`).classList.add('fa-times-circle');
		document.querySelector(`#grupo__password2 i`).classList.remove('fa-check-circle');
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
}


inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
});


continuarBoton.addEventListener("click", function(evento) {
	const inputPassword1 = document.getElementById('password');
	evento.preventDefault(); // Detener envío del formulario por defecto
	formulario.reportValidity(); // Verificar que todos los campos sean válidos
	if (formulario.checkValidity() && campos.password && campos.password2 && inputPassword1.value.trim() !== "") {
	  // Redirigir a la página de inicio si todo está bien
	  window.location.href = "pantalla_inicio.html";
	} else {
	  // Mostrar un mensaje de error si hay campos inválidos
	  alert("Complete el formulario para Continuar");
	}
  });

  
  
  
  
  

