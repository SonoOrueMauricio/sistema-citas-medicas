/*CALENDARIO INICIO */
document.addEventListener('DOMContentLoaded', function() {

    /* ===== CALENDARIO ===== */
    var calendarEl = document.getElementById('calendar');

    if (calendarEl) {
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',

            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: ''
            },

            locale: 'es',

            events: [
                { title: 'Cita Médica', date: '2026-05-25' },
                { title: 'Control', date: '2026-05-28' }
            ]
        });

        calendar.render();
    }


    /* ===== BLOQUEAR FECHAS PASADAS ===== */
    const fechaInput = document.getElementById('fecha');

    if (fechaInput) {
        const hoy = new Date().toISOString().split("T")[0];
        fechaInput.min = hoy;
    }

});

/* ==== CAMBIO DE SECCIONES (MENÚ) ==== */

const menuItems = document.querySelectorAll('.menu li');
const views = document.querySelectorAll('.view');

menuItems.forEach(item => {
    item.addEventListener('click', () => {

        // quitar activo del menú
        menuItems.forEach(i => i.classList.remove('active'));

        // agregar activo al seleccionado
        item.classList.add('active');

        // obtener sección
        const section = item.getAttribute('data-section');

        // ocultar todas las vistas
        views.forEach(v => v.classList.remove('active'));

        // mostrar la correspondiente
        document.getElementById(section).classList.add('active');

    });
});

const tabButtons = document.querySelectorAll('.tab-btn');
const tabViews = document.querySelectorAll('.tab-view');

tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {

        /* quitar activo */
        tabButtons.forEach(b => b.classList.remove('active'));
        tabViews.forEach(v => v.classList.remove('active'));

        /* activar seleccionado */
        btn.classList.add('active');
        document.getElementById(btn.dataset.tab).classList.add('active');

    });
});

/* ====== PERFIL USUARIO ====== */

const editBtn = document.getElementById('editBtn');
const saveBtn = document.getElementById('saveBtn');

/* inputs editables */
const editableInputs = document.querySelectorAll('.editable');

/* bloquear editables al inicio */
editableInputs.forEach(input => {
    input.disabled = true;
});

if (editBtn) {
    editBtn.addEventListener('click', () => {

        editableInputs.forEach(input => {
            input.disabled = false;
        });

        editBtn.style.display = 'none';
        saveBtn.style.display = 'block';

    });
}

if (saveBtn) {
    saveBtn.addEventListener('click', (e) => {

        e.preventDefault();

        editableInputs.forEach(input => {
            input.disabled = true;
        });

        editBtn.style.display = 'block';
        saveBtn.style.display = 'none';

        alert("Datos actualizados (simulado)");

    });
}

/*VALIDACIONES DE FORMULARIO / CITAS Y MENSAJES DE ERROR*/
/* ===== VALIDACIÓN FORMULARIO CITA ===== */

const form = document.getElementById('citaForm');

if (form) {

    form.addEventListener('submit', function(e) {

        e.preventDefault();

        let isValid = true;

        // obtener campos
        const descripcion = document.getElementById('descripcion');
        const especialidad = document.getElementById('especialidad');
        const fecha = document.getElementById('fecha');
        const hora = document.getElementById('hora');
        const medico = document.getElementById('medico');

        // limpiar errores
        document.querySelectorAll('.error-text').forEach(el => el.textContent = '');
        form.querySelectorAll('input, select, textarea').forEach(el => el.classList.remove('error'));

        // validar descripción
        if (descripcion.value.trim() === '') {
            mostrarError(descripcion, "Ingrese una descripción");
            isValid = false;
        }

        // validar especialidad
        if (especialidad.value === '') {
            mostrarError(especialidad, "Seleccione una especialidad");
            isValid = false;
        }

        // validaciones
        if (fecha.value === '') {
            mostrarError(fecha, "Seleccione una fecha");
            isValid = false;
        }

        if (hora.value === '') {
            mostrarError(hora, "Seleccione una hora");
            isValid = false;
        }

        if (medico.value === '') {
            mostrarError(medico, "Seleccione un médico");
            isValid = false;
        }

        if (isValid) {
            alert("Cita registrada correctamente (simulado)");
            form.reset();
        }

    });

}

/* función para mostrar error */
function mostrarError(input, mensaje) {

    input.classList.add('error');

    const errorText = input.parentElement.querySelector('.error-text');
    if (errorText) {
        errorText.textContent = mensaje;
    }
}
