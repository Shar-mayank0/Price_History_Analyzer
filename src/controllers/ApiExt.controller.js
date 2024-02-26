import { asynchandler } from "../utils/asynchandler.js";
import {ApiUrl} from "../models/ApiUrl.model.js";
import { apiError } from "../utils/ApiError.js";

const registerProduct = asynchandler(async (req, res) => {
        res.json({ message: "Product registered" });
        const body = req.body;
        console.log(body);
        const newProduct = {
                site: body.Product_site,
                prod_id: body.Product_ID,
                url: body.Product_URL,
        };
        const prodExists = await ApiUrl.findOne({
                $or: [{prod_id: newProduct.prod_id}, {url: newProduct.url}]
        })
        if (prodExists) {
                throw new apiError(409, 'Product ID or URL already exists');
        }
        if (!newProduct.prod_id || !newProduct.url || !newProduct.site) {
                throw new apiError(404, 'Product ID, URL or site are missing');
        }
        
        await ApiUrl.create(newProduct);
});

export { registerProduct }

