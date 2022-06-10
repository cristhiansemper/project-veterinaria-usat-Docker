function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
///////////////////////////////////////////////////////////////////////////
const btnModificarRaza=document.querySelector('#modificar-raza');
const btnAgregarRaza=document.querySelector('#registrar-raza');
const btnModalRaza=document.querySelector('#btn-modal-raza');
const inptDescripcion = document.querySelector("#id_descripcion")
const cboAnimal = document.querySelector("#id_id_tipo_mascota")

btnAgregarRaza.addEventListener('click',registrarRaza);
btnModificarRaza.addEventListener('click',modificarRaza);

$(document).ready(function(){
    listarRaza();
})
///////////////////////////////////////////////////////////////////////////


async function listarRaza(){
    try {
        const response = await fetch("/citas/listar_raza/");
        const result = await response.json();
        
        let resultado = result.raza

        if ($.fn.DataTable.isDataTable('#table-raza')) {
            $('#table-raza').DataTable().destroy();
        }
        $('#table-raza tbody').html("");
        for (i = 0; i < resultado.length; i++) {
            let fila = `<tr>`;
            fila += `<td>` + resultado[i][0] + `</td>`;
            fila += `<td>` + resultado[i][1] + `</td>`;
            fila += `<td>` + resultado[i][3] + `</td>`;
            if (resultado[i][2]) {
                fila += `<td><span class="badge bg-success">Activo</span></td>`;
            } else {
                fila += `<td><span class="badge bg-danger">Inactivo</span></td>`;
            }
            fila += `<td>
                            <div class="row">
                                <div class="form-group col-sm-4">
                                    <a href="#" class="btn-cargarDatos-modificar" data-toggle="modal" data-target="#modal-xl" onclick="cargarDatos('${resultado[i][0]}','${resultado[i][1]}','${resultado[i][2]}', '${resultado[i][3]}')">
                                        <i class="bi bi-pencil-square"></i>
                                    </a>                                   
                                </div>
                                <div class="form-group col-sm-4">
                                    <a href="#" class="btn-eliminar" onclick="eliminarRaza(${resultado[i][0]})">
                                        <i class="bi bi-trash"></i>
                                    </a>
                                </div>
                            </div>
                   </td>`;

            fila += `</tr>`;
            $('#table-raza tbody').append(fila);
        }
        $('#table-raza').DataTable({
            language: {
                decimal: "",
                emptyTable: "No hay información",
                info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                infoEmpty: "Mostrando 0 to 0 of 0 Entradas",
                infoFiltered: "(Filtrado de _MAX_ total entradas)",
                infoPostFix: "",
                thousands: ",",
                lengthMenu: "Mostrar _MENU_ Entradas",
                loadingRecords: "Cargando...",
                processing: "Procesando...",
                search: "Buscar:",
                zeroRecords: "Sin resultados encontrados",
                paginate: {
                    first: "Primero",
                    last: "Ultimo",
                    next: "Siguiente",
                    previous: "Anterior",
                },
            },
            lengthMenu: [5, 10, 20],
        })

    } catch (error) {
        console.log(error)
    }
}
///////////////////////////////////////////////////////////////////////////


async function registrarRaza(){
    const form = new FormData(document.querySelector('#form-raza'));
    form.set('descripcion',form.get('descripcion').trim());
    
    try {
        const response = await fetch('/citas/raza/',{
            method:'POST',
            body:form,
            headers:{'X-CSRFToken':getCookie('csrftoken')}
        });
        const result = await response.json()
        const {status} = result;
        const {mensaje} = result;
        if (status){
            listarRaza();
            imprimirMessage('Éxito',mensaje,'success');
            cleanData();
        }else{
            imprimirMessage('Sistema',mensaje,'info');
        }
    } catch (error) {
        console.log(error)
    }
}
///////////////////////////////////////////////////////////////////////////
let id_ra=0;
function cargarDatos(pk, desc, estado, animal){
    console.log(pk, desc, estado, animal)
    id_ra=pk;
    inptDescripcion.value = desc;
    cboAnimal.value = animal;
    if(estado){
        $("#id_estado").prop('checked', true);
    }else{
        $("#id_estado").prop('checked', false);
    }
    btnAgregarRaza.disabled=true;
    btnModificarRaza.disabled=false;
}

///////////////////////////////////////////////////////////////////////////

async function modificarRaza(){
    const form = new FormData(document.querySelector('#form-raza'));
    form.set('descripcion',form.get('descripcion').trim());
    form.append('id_raza',id_ra);
    try {
        const response = await fetch('/citas/modificar_raza/',{
            method:'POST',
            body:form,
            headers:{'X-CSRFToken':getCookie('csrftoken')}
        });
        const result = await response.json()
        const {status, mensaje} = result;

        if (status){
            listarRaza();
            imprimirMessage('Éxito',mensaje,'success');
            cleanData();
        }else{
            imprimirMessage('Sistema',mensaje,'info');
        }
    } catch (error) {
        console.log(error)
    }
}

function eliminarRaza(id) {
    Swal.fire({
        "title": "¿Estás seguro?",
        "text": "Esta acción no se puede revertir",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, cancelar",
        "confirmButtonText": "Sí, eliminar",
        "confirmButtonColor": "#dc3545"
    }).then(function (result){
        if (result.isConfirmed){
            confirmarEliminar(id);
        }
    })
}

async function confirmarEliminar(id){
    try {
        const response = await fetch("/citas/eliminar_raza/" + id + "/");
        const result = await response.json();
        const {status}=result;
        if (status){
            const{mensaje}=result;
            listarRaza();
            imprimirMessage("Éxito",mensaje,"success");
        }
    } catch (error) {
        console.log(error)
        imprimirMessage("Sistema","Error al eliminar tipo servicio","error");
    }
}


function imprimirMessage(title, message, icon) {
    Swal.fire({
        "title": title,
        "text": message,
        "icon": icon
    })
}

function cleanData(){
    id_ra = 0
    inptDescripcion.value = ''
    cboAnimal.value = ''
    btnAgregarRaza.disabled=false;
    btnModificarRaza.disabled=true;
}