import qrcode
import io
import base64


def get_qr_b64(data):
    _qr = qrcode.make(data)
    stream = io.BytesIO()
    _qr.save(stream, "png")
    b64 = base64.b64encode(stream.getvalue()).decode("utf-8")

    return f"data:image/png;base64,{b64}"
