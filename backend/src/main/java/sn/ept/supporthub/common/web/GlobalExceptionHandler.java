package sn.ept.supporthub.common.web;

import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

/**
 * Renders every API error as an RFC 7807 {@code ProblemDetail}. Feature-specific exceptions get
 * their own {@code @ExceptionHandler} methods here as they are introduced.
 */
@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {}
