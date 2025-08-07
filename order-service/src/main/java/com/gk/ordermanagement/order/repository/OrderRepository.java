package com.gk.ordermanagement.order.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.gk.ordermanagement.order.model.Order;

public interface OrderRepository extends JpaRepository<Order, String> {

}
