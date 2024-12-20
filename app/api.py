from fastapi import APIRouter, HTTPException, Depends
from tortoise.exceptions import DoesNotExist
from app.core.security import hash_password, verify_password, create_access_token, pwd_context
from app.db.session import init_db
from tortoise.contrib.pydantic import pydantic_model_creator


from app.models import (
    User_Pydantic,
    User_PydanticIn,
    Product_Pydantic,
    Product_PydanticIn,
    Order_Pydantic,
    Order_PydanticIn,
    Shipping_Pydantic,
    Shipping_PydanticIn,
    ShippingCompany_Pydantic,
    ShippingCompany_PydanticIn,
    Tutorial_Pydantic,
    Tutorial_PydanticIn,
)
from app.models import (
    User, 
    Product, 
    Order, 
    Shipping, 
    ShippingCompany, 
    Tutorial,
    BusinessOwner
)
from app.schemas import (
    UserCreate, 
    LoginRequest, 
    UserResponse, 
    ProductCreate, 
    ProductResponse, 
    OrderCreate, 
    OrderResponse, 
    ShippingCreate, 
    ShippingResponse, 
    ShippingCompanyCreate, 
    ShippingCompanyResponse, 
    TutorialCreate, 
    TutorialResponse,
    BusinessOwnerResponse,
    BusinessOwnerCreate
)




# router api
router = APIRouter()


# User Endpoints
@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    await init_db()
    
    try:
        db_user = await User.get(email=user.email)
        raise HTTPException(status_code=400, detail="Email already registered")
    except DoesNotExist:
        pass

    hashed_password = hash_password(user.password)
    new_user = await User.create(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    
    return new_user



@router.post("/register/business_owner", response_model=BusinessOwnerResponse)
async def register_business_owner(business_owner_data: BusinessOwnerCreate):
    # Check if the email already exists in the system
    existing_user = await User.get_or_none(email=business_owner_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Hash the password provided by the user
    hashed_password = pwd_context.hash(business_owner_data.password)

    # Create a new user with the role "business_owner"
    user = User(
        name=business_owner_data.business_name,  # Use business_name as user name for simplicity
        email=business_owner_data.email,  # Use email as user identifier
        hashed_password=hashed_password,  # Store the hashed password
        role="business_owner"
    )

    # Save the user
    await user.save()

    
    """
    Create the business owner profile,
    this allow user to register as business owner, in 
    """
    business_owner_profile = BusinessOwner(
        business_name=business_owner_data.business_name,
        description=business_owner_data.description,  # Handle optional description
        email=business_owner_data.email,
        phone=business_owner_data.phone,
        address=business_owner_data.address,
        user_id=user.id  # Associate the user with the business owner profile
    )

    # Save the business owner profile
    await business_owner_profile.save()

    # Return the business owner response model
    return BusinessOwnerResponse.from_orm(business_owner_profile)



@router.post("/token")
async def login_for_access_token(login_request: LoginRequest):
    await init_db()
    
    try:
        # Get the user from the database by email
        db_user = await User.get(email=login_request.email)
        
        # Verify the password
        if not verify_password(login_request.password, db_user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid credentials")
    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Generate the access token
    access_token = create_access_token(data={"sub": db_user.email})
    
    # Return the access token and token type
    return {"access_token": access_token, "token_type": "bearer"}




# Product Endpoints
@router.post("/products", response_model=ProductResponse)
async def create_product(product: ProductCreate):
    # Check if the seller exists
    try:
        seller = await BusinessOwner.get(id=product.seller_id)
    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Seller does not exist")

    # Create a new product
    db_product = await Product.create(
        name=product.name,
        category=product.category,
        price=product.price,
        quantity=product.quantity,
        description=product.description,
        seller_id=product.seller_id  # Ensure the foreign key relationship is maintained
    )

    # Return the created product as a response using ProductResponse
    return ProductResponse.from_orm(db_product)


@router.get("/products", response_model=list[Product_Pydantic])
async def get_products(skip: int = 0, limit: int = 100):
    """
    Get a list of products with pagination.
    - skip: The number of records to skip (default is 0).
    - limit: The maximum number of records to return (default is 100).
    """
    products = await Product_Pydantic.from_queryset(Product.all().offset(skip).limit(limit))
    
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    
    return products




# Order Endpoints

@router.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate):
    try:
        order_obj = await Order.create(**order.dict())
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation Error: {e.errors()}"
        )
    return OrderResponse.from_orm(order_obj)


@router.get("/orders", response_model=list[Order_Pydantic])
async def get_orders(skip: int = 0, limit: int = 100):
    """
    Get a list of products with pagination.
    - skip: The number of records to skip (default is 0).
    - limit: The maximum number of records to return (default is 100).
    """
    orders = await Order_Pydantic.from_queryset(Order.all().offset(skip).limit(limit))
    
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    
    return orders



# Shipping Endpoints
@router.post("/shipping", response_model=ShippingResponse)
async def create_shipping(shipping: ShippingCreate):
    try:
        shipping_obj = await shipping.create(**shipping.dict())
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation Error: {e.errors()}"
        )
    return ShippingResponse.from_orm(shipping_obj)





@router.get("/shipping", response_model=list[Shipping_Pydantic])
async def get_shipping(skip: int = 0, limit: int = 100):
    """
    Get a list of products with pagination.
    - skip: The number of records to skip (default is 0).
    - limit: The maximum number of records to return (default is 100).
    """
    shipping = await Shipping_Pydantic.from_queryset(Shipping.all().offset(skip).limit(limit))
    
    if not shipping:
        raise HTTPException(status_code=404, detail="No shipping found")
    
    return shipping





"""
here we allow shipping and delivery companies to register
"""
# ShippingCompany Endpoints
@router.post("/register-shipping-company", response_model=ShippingCompanyResponse)
async def create_shipping_company(shipping_company_data: ShippingCompanyCreate):

  
    # Check if the email already exists in the system
    existing_user = await User.get_or_none(email=shipping_company_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Hash the password provided by the user
    hashed_password = pwd_context.hash(shipping_company_data.password)

    # Create a new user with the role "business_owner"
    user = User(
        name=shipping_company_data.name,  # Use business_name as user name for simplicity
        email=shipping_company_data.email,  # Use email as user identifier
        hashed_password=hashed_password,  # Store the hashed password
        role="business_owner"
    )

    # Save the user
    await user.save()


    """
    Create the business owner profile,
    this allow user to register as business owner, in 
    """
    shipping_company_profile = ShippingCompany(
        name=shipping_company_data.name,
        email=shipping_company_data.email,
        contact=shipping_company_data.contact,
        address=shipping_company_data.address,
        user_id=user.id  # Associate the user with the business owner profile
    )


    await shipping_company_profile.save()

    return ShippingCompanyResponse.from_orm(shipping_company_profile)


# get all shipping companies
@router.get("/shipping-company", response_model=list[ShippingCompany_Pydantic])
async def get_shipping_companies(skip: int = 0, limit: int = 100):
    """
    Get a list of products with pagination.
    - skip: The number of records to skip (default is 0).
    - limit: The maximum number of records to return (default is 100).
    """
    shipping_companies = await ShippingCompany_Pydantic.from_queryset(ShippingCompany.all().offset(skip).limit(limit))
    
    if not shipping_companies:
        raise HTTPException(status_code=404, detail="No shipping company found")
    
    return shipping_companies




# Tutorial Endpoints (Learning Center)
@router.post("/tutorials", response_model=Tutorial_Pydantic)
async def create_tutorial(tutorial: Tutorial_PydanticIn):
    tutorial_obj = await Tutorial.create(**tutorial.dict())
    return await Tutorial_Pydantic.from_tortoise_orm(tutorial_obj)

@router.get("/tutorials", response_model=list[Tutorial_Pydantic])
async def get_tutorials():
    return await Tutorial_Pydantic.from_queryset(Tutorial.all())
