from src.core import board, auth

def run():
    issue1 = board.create_issue(
        email="mail1@gmail.com",
        title="Mi computadora no funciona",
        description="Me compraron una nueva pc y no anda"
    )

    issue2 = board.create_issue(
        email="mail2@gmail.com",
        title="No puedo obtener mis mails",
        description="Estoy tratando de acceder a los mails",
        status="in_progress"
    )

    issue3 = board.create_issue(
        email="mail3@gmail.com",
        title="No puedo imprimir",
        description="No anda la impresora",
        status="done"
    )
    fede = auth.create_user(email="fede@gmail.com", password="1234")    
    mati = auth.create_user(email="mati@gmail.com", password="1234")    
    miguel = auth.create_user(email="miguel@gmail.com", password="1234")        

    board.assign_user(issue1, fede)
    board.assign_user(issue2, mati)
    board.assign_user(issue3, miguel)

    label1 = board.create_label(title="Urgente",description="Issues que tienen que resolverse dentro de 24hs",)
    label2 = board.create_label(title="Importante",description="Issues de alta prioridad",)
    label3 = board.create_label(title="Soporte",description="Issues relacionados con soporte técnico",)
    label4 = board.create_label(title="Ventas",description="Issues relacionados con el área de ventas",)

    board.assign_labels(issue1, [label1, label2])
    board.assign_labels(issue2, [label3, label4])
    board.assign_labels(issue3, [label1, label3])