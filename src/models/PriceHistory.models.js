// Import the mongoose module
import mongoose, {Schema} from "mongoose";

// Create a new schema for the ApiPriceHistory model

const PriceHistorySchema = new Schema({
    site: {
        type: String,
        required: true,
        index: true
    },
    prod_id: {
        type: String,
        required: true,
        index: true
    },
    price: {
        type: [Number],
        required: true
    },
    date: {
        type: [Date],
        required: true
    },
    highst: {
        type: [Number],
        required: true
    },
    lowst: {
        type: [Number],
        required: true
    },
    ymin: {
        type: Number,
        required: true
    }

});

// Create a new model for the PriceHistorySchema and export it
export const PriceHistory = mongoose.model("PriceHistory", PriceHistorySchema); 