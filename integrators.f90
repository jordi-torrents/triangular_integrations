subroutine compute_forces(F, num1, num2, N, x)
  implicit none
  integer :: i
  integer, intent(in) :: N
  real(8), intent(in):: num1(0:N), num2(0:N), x(0:N)
  real(8), intent(inout) :: F(0:N)
  ! assuming g/M=1

  F(0) = -2.d0*(-num2(0)/((x(0)-x(1))*0.5d0*(x(0)+x(1))*(x(0)-x(1))))

  do i=1,N-1
    F(i)=-2.d0*((num1(i)/((x(i-1)-x(i))*0.5d0*(x(i-1)+x(i))*(x(i-1)-x(i+1))))&
               -(num2(i)/((x(i)-x(i+1))*0.5d0*(x(i+1)+x(i))*(x(i-1)-x(i+1)))))
  end do

  F(N) = -2.d0*((num1(N)/((x(N-1)-x(N))*0.5d0*(x(N)+x(N-1))*x(N-1)))-num2(N)/(x(N)*0.5d0*x(N)*x(N-1)))
end subroutine

subroutine Velocity_Verlet_steps(steps, v, x, num1, num2, N, dt)
  implicit none
  integer :: steps, i, N
  real(8) :: F(0:N), v(0:N), x(0:N), num1(0:N), num2(0:N), dt

  call compute_forces(F, num1, num2, N, x)
  v = v + F*0.5d0*dt
  do i=1,steps
    x = x + v*dt
    call compute_forces(F, num1, num2, N, x)
    v = v + F*dt
  end do
  v = v - F*0.5d0*dt

end subroutine

subroutine PEFRL_steps(steps, v, x, num1, num2, N, dt)
  ! https://doi.org/10.1016/S0010-4655(02)00451-4
  implicit none
  integer :: i, N
  integer, intent(in):: steps
  real(8), intent(inout) :: v(0:N), x(0:N)
  real(8), intent(in) :: num1(0:N), num2(0:N), dt
  real(8) :: F(0:N)
  real(8) :: xi = .1786178958448091d0,&
             la =-.2123418310626054d0,&
             ji =-.6626458266981849d-1

  x=x+v*xi*dt
  do i=1,steps
    call compute_forces(F, num1, num2, N, x)
    v=v+(0.5d0-la)*dt*F
    x=x+ji*dt*v
    call compute_forces(F, num1, num2, N, x)
    v=v+la*dt*F
    x=x+(1.d0-2.d0*(ji+xi))*dt*v
    call compute_forces(F, num1, num2, N, x)
    v=v+la*dt*F
    x=x+ji*dt*v
    call compute_forces(F, num1, num2, N, x)
    v=v+F*(0.5d0-la)*dt
    x=x+2.d0*xi*v*dt
  end do
  x=x-v*xi*dt
end subroutine
