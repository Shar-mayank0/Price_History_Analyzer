import { Router } from "express";
import {regpriceHistory, getPriceHistory, getPriceHistoryById, getPriceHistoryBySite } from "../controllers/priceHistory.controller.js";

/**
 * Express router instance.
 * @type {Router}
 */
const router = Router();
router.route("/pricehistory/register").post(regpriceHistory);
router.route("/pricehistory").get(getPriceHistory);
router.route("/pricehistory/:prod_id").get(getPriceHistoryById);
router.route("/pricehistory/:site").get(getPriceHistoryBySite);

export default router;
