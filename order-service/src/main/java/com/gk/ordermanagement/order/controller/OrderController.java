package com.gk.ordermanagement.order.controller;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.gk.ordermanagement.order.model.Order;
import com.gk.ordermanagement.order.repository.OrderRepository;

@RestController
@RequestMapping("/orders")
public class OrderController {

	private static final Logger logger = LoggerFactory.getLogger(OrderController.class);

	@Autowired
	private OrderRepository repo;

	@GetMapping
	public List<Order> getOrders() {
		logger.info("Pulling all the orders from DB");
		return repo.findAll();
	}
}
