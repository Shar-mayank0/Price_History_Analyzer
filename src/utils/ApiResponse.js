class ApiResponse {
    constructor(statuCode, message = "success", data) {
        this.statuCode  = statuCode;
        this.message = message;
        this.success = statuCode < 400;
        this.data = data;
    }
}