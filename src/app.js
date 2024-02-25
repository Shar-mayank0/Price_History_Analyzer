import  express from "express";
import cors from "cors";
import cookieParser from "cookie-parser";

const app = express();

app.use(cors({
    origin: process.env.CLIENT_URL || "http://localhost:3000",
    credentials: true
}));

app.use(express.json({
    limit: "50mb"
}));
app.use(express.urlencoded({
    extended: true,
    limit: "50mb"
}));
app.use(express.static("public"));
app.use(cookieParser());

 // Import ApiExt.routes module
import apiExtRouter  from "./routes/ApiExt.routes.js";

app.use("/api/v1/ext", apiExtRouter);

export { app } 
