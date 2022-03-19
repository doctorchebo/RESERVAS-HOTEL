Se propone crear los siguientes endpoints:

reservas
reservas/item
reservas/item/{id}

clientes
clientes/{id}

cuartos
cuartos/{id}

facturas
facturas/{id}

Todavía falta crear la lógica para crear las reservas pero la base ya está lista.

1) Se añaden items de reserva (esto permite reservas varias habitaciones en una sola reserva)
2) Se crea la reserva, anotando los datos del clientes
3) Se emite la factura, en base a la información de los items de reserva

Los otros endpoints sirven para ver y modificar los datos de las habitaciones y de los clientes

