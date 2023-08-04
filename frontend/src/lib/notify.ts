import Toastify from 'toastify-js'

const _console_log = window.console.log

export function dbg(...msg: any) {
    _console_log(...msg)

    let myMsg = ""
    for (const part of msg) {
        if (typeof part === "object") {
            myMsg += JSON.stringify(part) + " "
        } else
            myMsg += part.toString() + " "
    }

    Toastify({
        text: myMsg,
        duration: 5000,
        newWindow: true,
        close: true,
        gravity: "bottom", // `top` or `bottom`
        position: "right", // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
            // Tabler bg
            background: "var(--tblr-card-bg-hover)",
        }
    }).showToast();
}

window.console.log = dbg