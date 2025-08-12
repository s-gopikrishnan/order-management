package com.gk.ordermanagement.edge.controller;

import java.time.LocalDateTime;
import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.gk.ordermanagement.common.models.BaseEvent;
import com.gk.ordermanagement.common.models.OrderPlacedEvent;
import com.gk.ordermanagement.common.models.OrderRequest;

@RestController
@RequestMapping("/orders")
public class OrderController {

	private static final Logger logger = LoggerFactory.getLogger(OrderController.class);

	@Autowired
	private KafkaTemplate<String, BaseEvent> kafkaTemplate;

	@PostMapping
	public ResponseEntity<?> placeOrder(@RequestBody OrderRequest request) {
		String correlationId = UUID.randomUUID().toString();
		logger.info("[{}] Processing order request: {}", correlationId, request);
		request.setOrderId(correlationId);
		request.setPlacedTime(LocalDateTime.now());

		OrderPlacedEvent event = new OrderPlacedEvent(correlationId, request);
		kafkaTemplate.send("order-placed", event.getOrderId(), event);
		return ResponseEntity.accepted().body("Order accepted");
	}

	@GetMapping("/health")
	public String getHealth() {
		return "All good here";
	}

}
