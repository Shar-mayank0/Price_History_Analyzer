class apiError extends Error {
    constructor(statusCode, message, stack = '', errors = []) {
        super(message);
        this.statusCode = statusCode;
        this.errors = errors;
        this.data = null;
        this.message = message;
        this.succecss = false;
        this.status = `${statusCode}`.startsWith('4') ? 'fail' : 'error';
        if (stack) {
        this.stack = stack;
        } else {
        Error.captureStackTrace(this, this.constructor);}
    }
}

export { apiError } // This is the named export for this module