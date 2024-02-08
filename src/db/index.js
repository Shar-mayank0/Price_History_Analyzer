import mongoose from "mongoose";
import { DB_NAME } from "../constants.js";

const connectDB = async () => {
    try {
        const connectDB = await mongoose.connect(
            `${process.env.MONGO_URI}/${DB_NAME}`
        );
        console.log(`MongoDB connection SUCCESS: ${connectDB.connection.host}`);
    } catch (error) {
        console.error("MongoDB connection FAIL", error);
        process.exit(1);
    }
};

export default connectDB  // This is the default export for this module