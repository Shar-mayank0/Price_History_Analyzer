import { asynchandler } from "../utils/asynchandler.js";
import {PriceHistory} from "../models/PriceHistory.models.js";
import { apiError } from "../utils/ApiError.js";

const regpriceHistory = asynchandler(async (req, res) => {
        const body = req.body;
        console.log(body);
        const newPrice = {
                site: body.site,
                prod_id: body.prod_id,
                price: body.prices,
                date: body.dates,
                ymin:body.yAxisTicksMin,
                highst:body.highestPrices,
                lowst:body.lowestPrices

        };
        if (!newPrice.prod_id || !newPrice.price || !newPrice.site || !newPrice.date) {
                throw new apiError(404, 'Product ID, price, site or date are missing');
        }
        await PriceHistory.create(newPrice);
        res.json({message: "price history registered"});
        console.log("price history registered in the DB")
});

const getPriceHistory = asynchandler(async (req, res) => {
        const allproducts = await PriceHistory.find();
        res.json(allproducts);
        console.log("getPriceHistory called successfully")
});

const getPriceHistoryById = asynchandler(async (req, res) => {
        let queryparam = req.query.prod_id;
        if(!queryparam)
        {
                throw new apiError(404, 'query param prod_id missing');
        }
        const product = await PriceHistory.find({prod_id: queryparam});
        if (!product) {
                throw new apiError(404, 'Product not found');
        }
        res.json(product);
        console.log("getPriceHistoryById called successfully")
});

const getPriceHistoryBySite = asynchandler(async (req, res) => {
        let queryparam = req.query.site;
        if(!queryparam)
        {
                throw new apiError(404, 'query param site missing');
        }
        const product = await PriceHistory.find({site: queryparam});
        if (!product) {
                throw new apiError(404, 'Product not found');
        }
        res.json(product);
        console.log("getPriceHistoryBySite called successfully")
});

export {regpriceHistory, getPriceHistory, getPriceHistoryById, getPriceHistoryBySite};