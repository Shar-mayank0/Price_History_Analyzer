import dotenv from "dotenv"; // Import the dotenv module
import connectDB from "./db/index.js";  // Import the default export from the db module

dotenv.config(
    {
        path: "./env"
    }
);  // Invoke the config method on the dotenv object

connectDB();

// Connect to MongoDB atlas

