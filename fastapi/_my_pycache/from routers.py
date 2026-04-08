from routers.users import router as users_router

# Include routers
app.include_router(users_router, prefix="/api", tags=["users"])