const ids = db.bienes.find({}, {_id:1}).toArray().map(d => d._id);

// Movimientos
db.movimientos.insertMany([
  {bien_id: ids[3], tipo:'ENTRADA', fecha:new Date('2024-01-10'), sede_origen:null, sede_destino:'ATL', motivo:'Incorporacion de laptop nueva por compra directa', autorizado_por:'Dir. Administracion', documento_soporte:'OC-2024-001', bien_codigo_inventario:'UNEG-ATL-03-00004', bien_descripcion:'Laptop HP EliteBook 840 G8'},
  {bien_id: ids[4], tipo:'ENTRADA', fecha:new Date('2023-08-22'), sede_origen:null, sede_destino:'JBO', motivo:'Incorporacion de laptop para Biblioteca Central', autorizado_por:'Dir. Administracion', documento_soporte:'OC-2023-045', bien_codigo_inventario:'UNEG-JBO-03-00005', bien_descripcion:'Laptop Dell Latitude 5520'},
  {bien_id: ids[0], tipo:'TRASLADO', fecha:new Date('2024-06-15'), sede_origen:'VAS', sede_destino:'ATL', motivo:'Reasignacion a nueva oficina administrativa', autorizado_por:'Jefe de Bienes', documento_soporte:'MEM-2024-012', bien_codigo_inventario:'UNEG-ATL-03-00001', bien_descripcion:'Computadora Dell OptiPlex 7090'},
  {bien_id: ids[2], tipo:'REASIGNACION', fecha:new Date('2024-03-10'), sede_origen:'VAS', sede_destino:'VAS', motivo:'Cambio de custodio por rotacion de personal', autorizado_por:'Coord. Registro', documento_soporte:'MEM-2024-008', bien_codigo_inventario:'UNEG-VAS-03-00003', bien_descripcion:'Computadora Lenovo ThinkCentre'},
  {bien_id: ids[24], tipo:'ENTRADA', fecha:new Date('2023-10-05'), sede_origen:null, sede_destino:'ATL', motivo:'Adquisicion de equipamiento de red para data center', autorizado_por:'Dir. Administracion', documento_soporte:'OC-2023-089', bien_codigo_inventario:'UNEG-ATL-03-00025', bien_descripcion:'Switch Cisco Catalyst 24 puertos'},
  {bien_id: ids[14], tipo:'TRASLADO', fecha:new Date('2024-02-20'), sede_origen:'ATL', sede_destino:'VAS', motivo:'Traslado de proyector para evento academico', autorizado_por:'Coord. Academica', documento_soporte:'MEM-2024-005', bien_codigo_inventario:'UNEG-ATL-04-00015', bien_descripcion:'Videoproyector Epson PowerLite E20'},
  {bien_id: ids[8], tipo:'SALIDA', fecha:new Date('2024-09-01'), sede_origen:'CHI', sede_destino:null, motivo:'Retiro para diagnostico en taller externo', autorizado_por:'Jefe de Bienes', documento_soporte:'MEM-2024-031', bien_codigo_inventario:'UNEG-CHI-03-00009', bien_descripcion:'Impresora Epson EcoTank L3250'}
]);
print('[OK] 7 movimientos insertados');

// Desincorporaciones
db.desincorporaciones.insertMany([
  {bien_id: ids[8], motivo:'INSERVIBILIDAD', justificacion_tecnica:'La impresora Epson EcoTank L3250 presenta fallo total del cabezal de impresion. Se realizaron dos intentos de reparacion sin exito. El costo de reemplazo supera el 70% del valor del equipo.', estado_proceso:'EN_REVISION', solicitado_por:'Miguel Torres', fecha_solicitud:new Date('2024-09-15'), validacion_ia:{cumple_criterios:true, observaciones:'Cumple criterios SUDEBIP'}, aprobado_por:null, fecha_aprobacion:null},
  {bien_id: ids[13], motivo:'OBSOLESCENCIA', justificacion_tecnica:'Silla de oficina con desgaste severo en mecanismo hidraulico y base de ruedas. Tapizado deteriorado con roturas multiples. Mas de 4 anos de uso, no justifica reparacion.', estado_proceso:'APROBADA', solicitado_por:'Roberto Blanco', fecha_solicitud:new Date('2024-08-20'), validacion_ia:{cumple_criterios:true, observaciones:'Cumple criterios SUDEBIP'}, aprobado_por:'Jefe de Bienes Nacionales', fecha_aprobacion:new Date('2024-10-05')}
]);
print('[OK] 2 desincorporaciones insertadas');

// Marcar bien como DESINCORPORADO
db.bienes.updateOne({_id: ids[13]}, {$set: {estado: 'DESINCORPORADO'}});

// Resumen
print('=== RESUMEN ===');
print('Bienes: ' + db.bienes.countDocuments());
print('Movimientos: ' + db.movimientos.countDocuments());
print('Desincorporaciones: ' + db.desincorporaciones.countDocuments());
