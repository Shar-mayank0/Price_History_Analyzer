import mongoose,{Schema} from "mongoose";

const ApiUrlSchema = new Schema({
    site: {
        type: String,
        required: true,
        index: true
    },
    prod_id: {
        type: String,
        required: true,
        unique: true,
        index: true
    },
    url: {
        type: String,
        required: true
    }
});

 // Create a new model for the ApiUrlSchema and export it
export const ApiUrl = mongoose.model("ApiUrl", ApiUrlSchema);