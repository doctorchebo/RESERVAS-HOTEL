Se propone crear los siguientes endpoints:

reservas
reservas/booking
reservas/booking/{id}

clientes
clientes/{id}

habitaciones
habitaciones/{id}

facturas
facturas/{id}

1) Se crea una reserva con los datos del cliente. Si el cliente ya tiene un id, se crea la reserva solo con el id del cliente
2) Se elige una habitacion para reservar, con una fecha de ingreso y otra de salida. El sistema no permite que se reserve una habitación si ésta ya está reservada en el rango que se desea reservar.
3) En el endpoint de facturas, se puede emitir factura de aquellas reservas que aún no se haya emitido la factura
4) En el endpoint de habitaciones, se puede cambiar los precios y nombres de las habitaciones

