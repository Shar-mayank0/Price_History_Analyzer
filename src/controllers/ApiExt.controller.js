import { asynchandler } from "../utils/asynchandler.js";
import {ApiUrl} from "../models/ApiUrl.model.js";

const registerProduct = asynchandler(async (req, res) => {
        res.json({ message: "Product registered" });
});

export { registerProduct }

