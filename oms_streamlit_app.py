import streamlit as st
import requests
import json
import time
import uuid
from datetime import datetime
import pandas as pd

# Configure the page
st.set_page_config(
    page_title="Order Management System",
    page_icon="🛒",
    layout="wide"
)

# Sample product catalog
PRODUCTS = {
    "item1": {"name": "Premium Laptop", "price": 1299.99, "description": "High-performance laptop with 16GB RAM"},
    "item2": {"name": "Wireless Mouse", "price": 29.99, "description": "Ergonomic wireless mouse with USB receiver"},
    "item3": {"name": "Mechanical Keyboard", "price": 149.99, "description": "RGB mechanical keyboard with blue switches"},
    "item4": {"name": "4K Monitor", "price": 399.99, "description": "27-inch 4K UHD monitor with HDR support"},
    "item5": {"name": "USB-C Hub", "price": 79.99, "description": "7-in-1 USB-C hub with HDMI and USB 3.0 ports"},
    "item6": {"name": "Webcam HD", "price": 89.99, "description": "1080p HD webcam with auto-focus"},
}

# API endpoints
ORDER_SUBMIT_URL = "http://localhost:8090/orders"
ORDER_RETRIEVE_URL = "http://localhost:8094/orders"

# Constant customer ID
CUSTOMER_ID = "OMS-Cust-001"

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'last_order_id' not in st.session_state:
    st.session_state.last_order_id = None

def add_to_cart(product_id):
    """Add product to cart"""
    if product_id in st.session_state.cart:
        st.session_state.cart[product_id] += 1
    else:
        st.session_state.cart[product_id] = 1

def remove_from_cart(product_id):
    """Remove product from cart"""
    if product_id in st.session_state.cart:
        if st.session_state.cart[product_id] > 1:
            st.session_state.cart[product_id] -= 1
        else:
            del st.session_state.cart[product_id]

def calculate_total():
    """Calculate total amount in cart"""
    total = 0
    for product_id, quantity in st.session_state.cart.items():
        total += PRODUCTS[product_id]["price"] * quantity
    return total

def submit_order():
    """Submit order to the API"""
    if not st.session_state.cart:
        st.error("Cart is empty!")
        return None
    
    product_ids = []
    for product_id, quantity in st.session_state.cart.items():
        product_ids.extend([product_id] * quantity)
    
    order_data = {
        "customerId": CUSTOMER_ID,
        "totalAmount": calculate_total(),
        "productIds": product_ids
    }
    
    try:
        response = requests.post(
            ORDER_SUBMIT_URL,
            headers={'Content-Type': 'application/json'},
            json=order_data,
            timeout=10
        )
        
        if response.status_code == 202 or response.status_code == 200 or response.status_code == 201:
            order_info = {
                "customer_id": CUSTOMER_ID,
                "order_data": order_data,
                "submit_time": datetime.now(),
                "status": "Submitted",
                "processing_time": None,
                "order_id": None,
                "placed_time": None,
                "confirmed_time": None
            }
            st.session_state.orders.append(order_info)
            st.session_state.cart = {}  # Clear cart
            st.success(f"Order submitted successfully! Customer ID: {CUSTOMER_ID}")
            return CUSTOMER_ID
        else:
            st.error(f"Failed to submit order. Status: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.warning("⚠️ Unable to connect to order service. Order simulated locally.")
        # Simulate order submission for demo purposes
        order_info = {
            "customer_id": CUSTOMER_ID,
            "order_data": order_data,
            "submit_time": datetime.now(),
            "status": "Submitted (Simulated)",
            "processing_time": None,
            "order_id": f"sim-{uuid.uuid4().hex[:8]}",
            "placed_time": None,
            "confirmed_time": None
        }
        st.session_state.orders.append(order_info)
        st.session_state.cart = {}
        st.success(f"Order simulated successfully! Customer ID: {CUSTOMER_ID}")
        return CUSTOMER_ID
    except Exception as e:
        st.error(f"Error submitting order: {str(e)}")
        return None

def fetch_all_orders():
    """Fetch all orders from the retrieval endpoint"""
    try:
        response = requests.get(ORDER_RETRIEVE_URL, timeout=10)
        if response.status_code == 200:
            orders_data = response.json()
            
            # Calculate processing time for each order
            processed_orders = []
            for api_order in orders_data:
                order_with_time = api_order.copy()
                
                # Calculate processing time from timestamps
                if (api_order.get("placedTime") and api_order.get("confirmedTime")):
                    try:
                        placed_dt = datetime.fromisoformat(
                            api_order["placedTime"].replace('Z', '+00:00')
                        )
                        confirmed_dt = datetime.fromisoformat(
                            api_order["confirmedTime"].replace('Z', '+00:00')
                        )
                        processing_time = (confirmed_dt - placed_dt).total_seconds()
                        order_with_time["processing_time"] = processing_time
                    except Exception as e:
                        st.error(f"Error parsing timestamps for order {api_order.get('id', 'unknown')}: {e}")
                        order_with_time["processing_time"] = None
                else:
                    order_with_time["processing_time"] = None
                
                processed_orders.append(order_with_time)
            
            return processed_orders
                        
    except requests.exceptions.ConnectionError:
        st.warning("⚠️ Unable to connect to order retrieval service.")
        return []
                    
    except Exception as e:
        st.error(f"Error fetching orders: {str(e)}")
        return []
    
    return []

# Main UI
st.title("🛒 Order Management System")

# Create tabs
tab1, tab2, tab3 = st.tabs(["🛍️ Shop", "🛒 Cart", "📋 Orders"])

with tab1:
    st.header("Product Catalog")
    
    # Display products in a grid
    cols = st.columns(3)
    for i, (product_id, product) in enumerate(PRODUCTS.items()):
        with cols[i % 3]:
            st.subheader(product["name"])
            st.write(product["description"])
            st.write(f"**Price: ${product['price']:.2f}**")
            
            if st.button(f"Add to Cart", key=f"add_{product_id}"):
                add_to_cart(product_id)
                st.success(f"Added {product['name']} to cart!")
                st.rerun()

with tab2:
    st.header("Shopping Cart")
    
    if st.session_state.cart:
        # Display cart items
        for product_id, quantity in st.session_state.cart.items():
            product = PRODUCTS[product_id]
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            
            with col1:
                st.write(f"**{product['name']}**")
                st.write(f"${product['price']:.2f} each")
            
            with col2:
                st.write(f"Qty: {quantity}")
            
            with col3:
                st.write(f"${product['price'] * quantity:.2f}")
            
            with col4:
                if st.button("➕", key=f"inc_{product_id}"):
                    add_to_cart(product_id)
                    st.rerun()
            
            with col5:
                if st.button("➖", key=f"dec_{product_id}"):
                    remove_from_cart(product_id)
                    st.rerun()
            
            st.divider()
        
        # Display total
        total = calculate_total()
        st.subheader(f"**Total: ${total:.2f}**")
        
        # Place order button
        if st.button("🚀 Place Order", type="primary", use_container_width=True):
            customer_id = submit_order()
            if customer_id:
                st.rerun()
    else:
        st.info("Your cart is empty. Add some products from the Shop tab!")

with tab3:
    st.header("All Orders from Backend")
    
    # Auto-refresh button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 Refresh Orders"):
            st.rerun()
    
    with col2:
        auto_refresh = st.checkbox("Auto-refresh every 3 seconds")
    
    if auto_refresh:
        time.sleep(3)
        st.rerun()
    
    # Fetch all orders from the backend
    all_orders = fetch_all_orders()
    
    if all_orders:
        # Create a dataframe for better display
        orders_data = []
        for order in all_orders:
            processing_time_str = "N/A"
            if order.get('processing_time') is not None:
                if order['processing_time'] < 1:
                    processing_time_str = f"{order['processing_time']*1000:.0f}ms"
                else:
                    processing_time_str = f"{order['processing_time']:.3f}s"
            
            orders_data.append({
                "Order ID": order.get("id", "N/A"),
                "Customer ID": order.get("customerId", "N/A"),
                "Amount": f"${order.get('amount', 0):.2f}",
                "Status": order.get("status", "UNKNOWN"),
                "Processing Time": processing_time_str,
                "Placed Time": order.get("placedTime", "N/A"),
                "Confirmed Time": order.get("confirmedTime", "N/A")
            })
        
        df = pd.DataFrame(orders_data)
        st.dataframe(df, use_container_width=True)
        
        # Show detailed order information
        st.subheader("Detailed Order Information")
        
        # Show statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Orders", len(all_orders))
        
        with col2:
            confirmed_orders = [o for o in all_orders if o.get('status') == 'CONFIRMED']
            st.metric("Confirmed Orders", len(confirmed_orders))
        
        with col3:
            processing_times = [o.get('processing_time') for o in all_orders if o.get('processing_time') is not None]
            if processing_times:
                avg_time = sum(processing_times) / len(processing_times)
                if avg_time < 1:
                    st.metric("Avg Processing", f"{avg_time*1000:.0f}ms")
                else:
                    st.metric("Avg Processing", f"{avg_time:.3f}s")
            else:
                st.metric("Avg Processing", "N/A")
        
        with col4:
            if processing_times:
                min_time = min(processing_times)
                if min_time < 1:
                    st.metric("Fastest", f"{min_time*1000:.0f}ms")
                else:
                    st.metric("Fastest", f"{min_time:.3f}s")
            else:
                st.metric("Fastest", "N/A")
        
        # Display individual order details
        for order in reversed(all_orders[-10:]):  # Show last 10 orders
            status_icon = "✅" if order.get('status') == 'CONFIRMED' else "❓"
            order_id = order.get('id', 'Unknown')
            customer_id = order.get('customerId', 'Unknown')
            
            with st.expander(f"{status_icon} Order {order_id} - {customer_id}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Order ID:** {order.get('id', 'N/A')}")
                    st.write(f"**Customer ID:** {order.get('customerId', 'N/A')}")
                    st.write(f"**Amount:** ${order.get('amount', 0):.2f}")
                    st.write(f"**Status:** {order.get('status', 'UNKNOWN')}")
                
                with col2:
                    if order.get('placedTime'):
                        placed_time = order['placedTime'].replace('Z', '').replace('T', ' ')[:19]
                        st.write(f"**Placed Time:** {placed_time}")
                    else:
                        st.write(f"**Placed Time:** N/A")
                    
                    if order.get('confirmedTime'):
                        confirmed_time = order['confirmedTime'].replace('Z', '').replace('T', ' ')[:19]
                        st.write(f"**Confirmed Time:** {confirmed_time}")
                    else:
                        st.write(f"**Confirmed Time:** N/A")
                    
                    if order.get('processing_time') is not None:
                        if order['processing_time'] < 1:
                            st.write(f"**Processing Time:** {order['processing_time']*1000:.0f}ms")
                        else:
                            st.write(f"**Processing Time:** {order['processing_time']:.3f}s")
                    else:
                        st.write("**Processing Time:** N/A")
    
    else:
        st.info("No orders found in the backend system.")
    
    # Separator for local orders
    st.divider()
    st.subheader("Local Cart Orders (Submitted from this session)")
    
    if st.session_state.orders:
        local_orders_data = []
        for order in st.session_state.orders:
            local_orders_data.append({
                "Customer ID": order["customer_id"],
                "Total Amount": f"${order['order_data']['totalAmount']:.2f}",
                "Items": len(order['order_data']['productIds']),
                "Status": order["status"],
                "Submit Time": order["submit_time"].strftime("%H:%M:%S")
            })
        
        local_df = pd.DataFrame(local_orders_data)
        st.dataframe(local_df, use_container_width=True)
    else:
        st.info("No orders submitted from this session yet. Start shopping!")

# Sidebar with system info
with st.sidebar:
    st.header("🔧 System Info")
    st.write("**API Endpoints:**")
    st.code(f"Submit: {ORDER_SUBMIT_URL}")
    st.code(f"Retrieve: {ORDER_RETRIEVE_URL}")
    
    st.write("**Customer ID:**")
    st.code(CUSTOMER_ID)
    
    st.write("**Cart Summary:**")
    if st.session_state.cart:
        for product_id, quantity in st.session_state.cart.items():
            st.write(f"• {PRODUCTS[product_id]['name']}: {quantity}")
        st.write(f"**Total: ${calculate_total():.2f}**")
    else:
        st.write("Cart is empty")
    
    st.write("**Order Statistics:**")
    
    # Get backend orders for statistics
    backend_orders = fetch_all_orders()
    total_backend_orders = len(backend_orders)
    local_orders = len(st.session_state.orders)
    
    st.write(f"• Backend Orders: {total_backend_orders}")
    st.write(f"• Local Session: {local_orders}")
    
    # Show average processing time from backend if available
    backend_processing_times = [
        o.get('processing_time') for o in backend_orders 
        if o.get('processing_time') is not None
    ]
    if backend_processing_times:
        avg_time = sum(backend_processing_times) / len(backend_processing_times)
        if avg_time < 1:
            st.write(f"• Backend Avg: {avg_time*1000:.0f}ms")
        else:
            st.write(f"• Backend Avg: {avg_time:.3f}s")
