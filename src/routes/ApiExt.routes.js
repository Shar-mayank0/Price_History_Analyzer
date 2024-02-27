import { Router } from "express";
import { registerProduct, getAllProducts, getProductById, deleteProductById, deleteAllProducts } from "../controllers/ApiExt.controller.js";

/**
 * Express router instance.
 * @type {Router}
 */
const router = Router();
router.route("/amazonproducts/url").post(registerProduct);
router.route("/flipkartproducts/url").post(registerProduct);
router.route("/amazonproducts/url").get(getAllProducts);
router.route("/flipkartproducts/url").get(getAllProducts);
router.route("/amazonproducts/url").get(getProductById);
router.route("/flipkartproducts/url").get(getProductById);
router.route("/amazonproducts/url").delete(deleteAllProducts);
router.route("/flipkartproducts/url").delete(deleteAllProducts);
router.route("/amazonproducts/url/:prod_id").delete(deleteProductById);
router.route("/flipkartproducts/url/:prod_id").delete(deleteProductById);

// This is the default export for this module
export default router;