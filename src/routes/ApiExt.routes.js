import { Router } from "express";
import { registerProduct } from "../controllers/ApiExt.controller.js";

const router = Router();

router.route("/amazonproducts/url/:prod_id").post(registerProduct);

// This is the default export for this module
export default router;