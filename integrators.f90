subroutine compute_forces(gm, F, num1, num2, N, x)
  implicit none
  integer :: i, N
  real(8) :: gm, const, F(0:N), num1(0:N), num2(0:N), x(0:N)
  const=-2.d0*gm

  F(0) = const*(-num2(0)/((x(0)-x(1))*0.5d0*(x(0)+x(1))*(x(0)-x(1))))

  do i=1,N-1
    F(i)=const*((num1(i)/((x(i-1)-x(i))*0.5d0*(x(i-1)+x(i))*(x(i-1)-x(i+1))))&
               -(num2(i)/((x(i)-x(i+1))*0.5d0*(x(i+1)+x(i))*(x(i-1)-x(i+1)))))
  end do

  F(N) = const*((num1(N)/((x(N-1)-x(N))*0.5d0*(x(N)+x(N-1))*x(N-1)))-num2(N)/(x(N)*0.5d0*x(N)*x(N-1)))
end subroutine

subroutine Velocity_Verlet_steps(steps, gm, v, x, num1, num2, N, dt)
  implicit none
  integer :: steps, i, N
  real(8) :: gm, F(0:N), v(0:N), x(0:N), num1(0:N), num2(0:N), dt

  call compute_forces(gm, F, num1, num2, N, x)
  v = v + F*0.5d0*dt
  do i=1,steps
    x = x + v*dt
    call compute_forces(gm, F, num1, num2, N, x)
    v = v + F*dt
  end do
  v = v - F*0.5d0*dt

end subroutine

subroutine PEFRL_steps(steps, gm, v, x, num1, num2, N, dt)
  ! https://doi.org/10.1016/S0010-4655(02)00451-4
  implicit none
  integer :: steps, i, N
  real(8) :: gm, F(0:N), v(0:N), x(0:N), num1(0:N), num2(0:N), dt
  real(8) :: xi = 0.1786178958448091d0,&
             la =-0.2123418310626054d0,&
             ji =-0.6626458266981849d-1

  x=x+v*xi*dt
  do i=1,steps
    call compute_forces(gm, F, num1, num2, N, x)
    v=v+(0.5d0-la)*dt*F
    x=x+ji*dt*v
    call compute_forces(gm, F, num1, num2, N, x)
    v=v+la*dt*F
    x=x+(1.d0-2.d0*(ji+xi))*dt*v
    call compute_forces(gm, F, num1, num2, N, x)
    v=v+la*dt*F
    x=x+ji*dt*v
    call compute_forces(gm, F, num1, num2, N, x)
    v=v+F*(0.5d0-la)*dt
    x=x+2.d0*xi*v*dt
  end do
  x=x-v*xi*dt
end subroutine
