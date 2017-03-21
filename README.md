# partner_contract_pricelist_cgt

This module adds following functionality:

	1) It adds "Product Pricelist" tab in Sales/Sales/Contracts form to configure Products.
	2) It adds new menu "Sales/Invoicing/Contracts Delivery Order" for creating Delivery Orders related to Contracts.
	3) On creating Delivery Order from above menu :
    	a) On Selecting Partner, user can select Contract related to selected Partner
    	b) If selected Contract has Only One Open Contract, it will get selected automatically
    	c) On selecting Contract, all "Product Pricelists" defined in the contract will get loaded in Move Lines
