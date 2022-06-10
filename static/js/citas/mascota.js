// Variables

let idCliente = document.querySelector("#txtbC")
let txtNombre = document.querySelector("#id_nombre")
let txtFechaNacimientoMascota = document.querySelector("#id_fecha_nacimiento")
let txtFechaRegistro = document.querySelector("#id_fecha_registro")
let txtEstado = document.querySelector("#id_estado")
let cboAnimall=document.querySelector('#id_animal');
let cboSexo=document.querySelector('#id_sexo');
let cboRaza=document.querySelector('#id_id_raza');

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
///////////////////////////////////////////////////////////////////////////
const btnModificarMascota=document.querySelector('#modificar-mascota');
const btnAgregarMascota=document.querySelector('#registrar-mascota');
const btnModalMascota=document.querySelector('#btn-modal-mascota');
const btnBuscarCliente=document.querySelector('#btnBuscarCliente');

btnBuscarCliente.addEventListener('click',buscarCliente);
btnModificarMascota.addEventListener('click',modificarMascota);
btnAgregarMascota.addEventListener('click',registrarMascota);

let pk_cliente=0;

async function buscarCliente(){
    try {
        const f=document.querySelector('#txtbC').value;
        console.log(f)
        const response = await fetch("/citas/buscar_cliente/"+f+"/");
        const result = await response.json();
        let resultado= JSON.parse(result.cliente)
        document.querySelector('#nombrecliente').value=resultado[0].fields.nombre+' '+resultado[0].fields.apellido
        pk_cliente=resultado[0].pk;
    } catch (error) {
        console.log(error);   
    }
}


///////////////////////////////////////////////////////////////////////////

$(document).ready(function(){
    listarMascota();
})

async function listarMascota(){
    try {
        const response = await fetch("/citas/listar_mascota/");
        const result = await response.json();

        console.log(result.mascota) // descripcion, estado
        
        let resultado = result.mascota
        console.log(resultado);
        if ($.fn.DataTable.isDataTable('#table-mascota')) {
            $('#table-mascota').DataTable().destroy();
        }
        $('#table-mascota tbody').html("");
        for (i = 0; i < resultado.length; i++) {
            let fila = `<tr>`;
            fila += `<td>` + resultado[i][0] + `</td>`;
            fila += `<td>` + resultado[i][1] + `</td>`;
            fila += `<td>` + resultado[i][2] + `</td>`;
            if (resultado[i][3]==1) {
                fila += `<td>Macho</td>`;
            } else {
                fila += `<td>Hembra</td>`;
            }
            fila += `<td>` + resultado[i][9] + `</td>`;
            fila += `<td>` + resultado[i][8] + `</td>`;
            fila += `<td>
                            <div class="row">
                                <div class="form-group col-sm-4">
                                    <a href="#" class="btn-cargarDatos-modificar" data-toggle="modal" data-target="#modal-xl" onclick="cargarDatos(
                                        ${resultado[i][0]}, '${resultado[i][1]}','${resultado[i][2]}',
                                        ${resultado[i][3]},'${resultado[i][4]}',${resultado[i][5]},${resultado[i][6]},
                                        ${resultado[i][7]} ,'${resultado[i][11]}', ${resultado[i][13]},
                                    )">
                                        <i class="bi bi-pencil-square"></i>
                                    </a>                                   
                                </div>
                                <div class="form-group col-sm-4">
                                    <a href="#" class="btn-eliminar" onclick="eliminarMascota('${resultado[i][0]}')">
                                        <i class="bi bi-trash"></i>
                                    </a>
                                </div>
                            </div>
                   </td>`;

            fila += `</tr>`;
            $('#table-mascota tbody').append(fila);
        }
        $('#table-mascota').DataTable({
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

async function registrarMascota(){
    console.log(document.querySelector('#id_user'))
    const form = new FormData(document.querySelector('#form-mascota'));
    form.set('nombre',form.get('nombre').trim());
    form.append('id_usuario',document.querySelector('#id_user').textContent);
    
    form.append('id_cliente',pk_cliente);
    try {
        const response = await fetch('/citas/mascota/',{
            method:'POST',
            body:form,
            headers:{'X-CSRFToken':getCookie('csrftoken')}
        });
        const result = await response.json()
        const {status} = result;
        const {mensaje} = result;
        if (status){
            listarMascota();
            imprimirMessage('Éxito',mensaje,'success');
            cleanData();
        }else{
            imprimirMessage('Sistema',mensaje,'info');
        }
    } catch (error) {
        console.log(error)
    }
}
let pk_mas=0;
function cargarDatos(pk, nombre_mas, fecha_nac,sexo,fecha_reg,estado,id_cliente,id_raza,dni, tm){
    pk_cliente=id_cliente;
    pk_mas=pk;
    console.log(pk_mas);
    idCliente.value=dni;
    cboAnimall.value=tm;
    txtNombre.value=nombre_mas;
    cboRaza.value=id_raza;
    cboSexo.value=sexo;
    txtFechaNacimientoMascota.value=fecha_nac;
    txtFechaRegistro.value=fecha_reg;
    if(estado){
        $("#id_estado").prop('checked', true);
    }else{
        $("#id_estado").prop('checked', false);
    }
    btnAgregarMascota.disabled=true;
    btnModificarMascota.disabled=false;
}

async function modificarMascota(){
    const form = new FormData(document.querySelector('#form-mascota'));
    form.set('nombre',form.get('nombre').trim());
    console.log(pk_cliente)
    form.append('id_cliente',pk_cliente);
    form.append('id_mascota',pk_mas);
    form.append('id_usuario',document.querySelector('#id_user').textContent);
    try {
        const response = await fetch('/citas/modificar_mascota/',{
            method:'POST',
            body:form,
            headers:{'X-CSRFToken':getCookie('csrftoken')}
        });
        const result = await response.json()
        const {status} = result;
        const {mensaje} = result;
        if (status){
            listarMascota();
            imprimirMessage('Éxito',mensaje,'success');
            cleanData();
        }else{
            imprimirMessage('Sistema',mensaje,'info');
        }
    } catch (error) {
        console.log(error)
    }
}


function eliminarMascota(id) {
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
        const response = await fetch("/citas/eliminar_mascota/" + id + "/");
        const result = await response.json();
        const {status}=result;
        if (status){
            const{mensaje}=result;
            listarMascota();
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
    
    btnAgregarMascota.disabled=false;
    btnModificarMascota.disabled=true;
}