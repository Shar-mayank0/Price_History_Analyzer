import dotenv from "dotenv"; // Import the dotenv module
import connectDB from "./db/index.js";  // Import the default export from the db module
import {app} from "./app.js"
dotenv.config(
    {
        path: "./env"
    }
);  // Invoke the config method on the dotenv object

// Connect to MongoDB atlas
connectDB()
.then(() => {
    app.on ("error", (err) => {
        console.error("Server Crashed due to: ", err);
    });
    app.listen(process.env.PORY || 3000, () => {
        console.log(`Server is running on port: ${process.env.PORT}`);
    });
})
.catch((err) => {
    console.error("MONGO DB connection FAILED!!", err);
});  // Call the connectDB function and handle the promise returned by it
